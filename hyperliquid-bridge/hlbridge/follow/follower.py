"""Copia su Hyperliquid la posizione che MultiCharts vuole. Non decide niente.

Le regole sono quelle dell'EA di MT5 (multicharts/bridge/SPEC.md, v2), tradotte:

- Agisce solo sui CAMBI della posizione voluta. Se lo stop d'emergenza chiude la posizione e
  MultiCharts non cambia, non la riapre.
- All'avvio non insegue niente: prende lo stato com'è e, se MultiCharts e Hyperliquid sono
  diversi, lo dice.
- Chiude il lato sbagliato e poi apre. Un cambio di size dentro un trade (stesso lato, più micro)
  non si copia.
- Fino a `tentativi` giri per ogni cambio, poi si ferma e avvisa, fino al cambio successivo.
- Una riga senza FINE, o un file che manca, non è uno stato: si rilegge al giro dopo.

Cosa aggiunge Hyperliquid: la posizione è una sola per perp (due strategie sullo stesso perp
non si possono seguire, vedi config.py), e ogni apertura passa dal motore di rischio. Una
chiusura passa sempre.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable

from hlbridge.follow.config import BridgeConfig
from hlbridge.follow.stato import Wanted, read_state
from hlbridge.journal.log import record as journal_record
from hlbridge.pm.notify import notify as pm_notify
from hlbridge.risk import engine
from hlbridge.schemas import OrderIntent

log = logging.getLogger(__name__)

DUST_USD = 1.0           # a residue under this is a rounding crumb, not a position


class Follower:
    def __init__(self, cfg: BridgeConfig, adapter, market, limits: dict, state, state_dir: Path,
                 journal: Callable = journal_record, notify: Callable = pm_notify,
                 venue_mid: Callable[[str], float | None] | None = None):
        self.cfg, self.adapter, self.market, self.limits, self.state = cfg, adapter, market, limits, state
        self.dir = Path(state_dir)
        self.journal, self.notify = journal, notify
        # Where the order will rest. The risk and liquidity rules read the main feed, but the size in dollars and the
        # stop price have to come from the venue: on testnet XYZ100 sat 13% away from mainnet (30,613 vs 26,995),
        # which would put a short's stop below the market and fire it on the spot.
        self.venue_mid = venue_mid
        self.last: dict[str, Wanted] = {}         # last state read, per strategy
        self.pending: dict[str, Wanted] = {}      # a change not carried out yet
        self.attempts: dict[str, int] = {}
        self._said: set[tuple[str, str]] = set()

    # ---- one pass ------------------------------------------------------------

    def step(self) -> None:
        for name, scfg in self.cfg.strategie.items():
            w = read_state(self.dir / scfg.file)
            if w is None:
                continue
            if w.strategy != name or w.instrument != scfg.strumento:
                self._once(name, "shape", f"{name}: il file dice {w.strategy}/{w.instrument}, "
                           f"la config vuole {name}/{scfg.strumento}: lo ignoro")
                continue
            if name not in self.last:
                self.last[name] = w
                self._baseline(name, w)
                continue
            if w.micro != self.last[name].micro:
                self.last[name] = w
                self.pending[name] = w
                self.attempts[name] = 0
                self.journal("follow_change", {"strategy": name, "micro": w.micro, "stop_pts": w.stop_pts})
                log.info("%s: MultiCharts vuole %+d micro", name, w.micro)
            if name in self.pending:
                self._apply(name)

    # ---- risk between orders --------------------------------------------------

    def watch_risk(self) -> None:
        """Fold the account's equity into the risk state: daily loss and drawdown are only seen if
        somebody looks while a position is open. A breach that asks to flatten closes the perps this
        bridge follows, and their orders. Not the rest of the account: a position the bridge did not
        open is not its to close (the manual kill switch of the UI still flattens everything). The loss
        is measured on the whole account, so another position's loss can still stop the bridge."""
        acc = self.adapter.account_state()
        fired = self.state.observe(acc.equity_usd, self.limits)
        if fired:
            self.notify(f"Rischio: {', '.join(fired)} ({self.state.halt_reason}).")
            self.journal("follow_risk", {"fired": fired, "halt_reason": self.state.halt_reason})
        if self.state.flatten_requested:
            closed = []
            for name in self.cfg.strategie:
                perp = self._perp(name)
                if self.adapter.close_position(perp, f"risk:{name}"):
                    closed.append(perp)
                self.adapter.cancel_asset_orders(perp)         # the stop of a closed position must not outlive it
            self.state.flatten_requested = False
            self.notify(f"Chiuse {len(closed)} posizioni del bridge ({', '.join(closed) or 'nessuna aperta'}) per il "
                        "limite di perdita; il resto del conto non è toccato. Il bridge non apre finché non lo sblocchi.")
            self.journal("follow_flatten", {"closed": closed})
        self.state.save()

    # ---- the start: look, don't chase ---------------------------------------

    def _baseline(self, name: str, w: Wanted) -> None:
        perp = self._perp(name)
        pos = self.adapter.account_state().position(perp)
        mine = pos.size if pos else 0.0
        target = self._target(name, w)
        same = (mine == 0 and target == 0) or (mine * target > 0)
        self.journal("follow_baseline", {"strategy": name, "micro": w.micro, "perp": perp, "perp_size": mine})
        if same:
            log.info("%s: all'avvio MultiCharts (%+d micro) e Hyperliquid (%+g) concordano", name, w.micro, mine)
        else:
            self.notify(f"{name}: all'avvio MultiCharts vuole {w.micro:+d} micro e su {perp} ci sono {mine:+g}. "
                        "Non inseguo: la posizione si allinea al prossimo cambio di MultiCharts.")

    # ---- carrying out a change ----------------------------------------------

    def _apply(self, name: str) -> None:
        w = self.pending[name]
        self.attempts[name] += 1
        if self.attempts[name] > self.cfg.tentativi:
            del self.pending[name]
            self.notify(f"{name}: dopo {self.cfg.tentativi} tentativi Hyperliquid non segue MultiCharts "
                        f"({w.micro:+d} micro). Mi fermo fino al cambio successivo.")
            self.journal("follow_gave_up", {"strategy": name, "micro": w.micro})
            return
        perp = self._perp(name)
        try:
            ctx = self.market.contexts()[perp]
        except KeyError:
            self.notify(f"{name}: {perp} non è tra i perp che vedo. Controlla il dex in HL_DEXS.")
            return
        acc = self.adapter.account_state()
        pos = acc.position(perp)
        if pos is not None and not pos.managed:
            del self.pending[name]
            self.notify(f"{name}: su {perp} c'è una posizione che non è nostra ({pos.size:+g}). Non la tocco.")
            self.journal("follow_foreign_position", {"strategy": name, "perp": perp, "size": pos.size})
            return
        px = self.venue_mid(perp) if self.venue_mid else None
        if self.venue_mid and not px:
            # Asked for a price from where the order rests and got none: ordering at the mainnet price would be the
            # exact mistake the venue price is there to avoid.
            self._once(name, "venue_mid", f"{name}: non vedo il book di {perp} dove devo ordinare: non ordino.")
            return
        if px:
            ctx = ctx.model_copy(update={"mid_px": px, "mark_px": px})
        target = self._target(name, w, ctx.sz_decimals)
        cur = pos.size if pos else 0.0
        if cur != 0 and abs(cur) * ctx.mid_px < DUST_USD:
            cur = 0.0

        if cur != 0 and target != 0 and cur * target > 0:
            del self.pending[name]
            log.info("%s: cambio di size dentro un trade, non si copia", name)
            return
        if cur != 0:                                     # wrong side, or flat wanted: close
            fill = self.adapter.close_position(perp, f"follow:{name}")
            self.adapter.cancel_asset_orders(perp)       # the old stop must not outlive the position
            self.journal("follow_close", {"strategy": name, "perp": perp, "filled": bool(fill)})
            if self._size(perp) != 0:
                return                                   # still open: try again next pass
        if target == 0:
            del self.pending[name]
            return
        self._open(name, w, perp, ctx, target)

    def _open(self, name: str, w: Wanted, perp: str, ctx, target: float) -> None:
        sign = 1 if target > 0 else -1
        px = ctx.mid_px
        stop_px = px - sign * w.stop_pts if w.stop_pts > 0 else None
        if stop_px is None:
            self.notify(f"{name}: MultiCharts non ha dato uno stop d'emergenza: apro senza.")
        # An IOC order is a limit: how far it may go from the mid is a setting, because a thin book (the testnet's
        # is 16% wide) is never reached by the adapter's default 20 bps. Size is units x that limit, so the
        # units are the ones MultiCharts' position asks for whatever the limit is.
        limit_px = px * (1 + sign * self.cfg.slittamento_max_bps / 1e4)
        intent = OrderIntent(asset=perp, side="buy" if sign > 0 else "sell", notional_usd=abs(target) * limit_px,
                             order_type="limit_ioc", limit_px=limit_px, stop_px=stop_px, strategy_id=name,
                             horizon_hours=0, reason=f"follow:{name}")
        acc = self.adapter.account_state()
        verdict = engine.evaluate(intent, acc, engine.Market(ctx), self.limits, self.state)
        if verdict.decision == "reject":
            self.notify(f"{name}: il rischio rifiuta l'apertura di {perp} ({', '.join(verdict.rules_fired)}). "
                        "MultiCharts è in posizione e Hyperliquid no.")
            self.journal("follow_rejected", {"strategy": name, "perp": perp, "rules": verdict.rules_fired})
            return
        if verdict.decision == "reduce":
            self.notify(f"{name}: il rischio riduce {perp} da ${intent.notional_usd:,.0f} a "
                        f"${verdict.approved_notional_usd:,.0f} ({', '.join(verdict.rules_fired)}).")
        fill = self.adapter.execute(intent, verdict, px)
        self.journal("follow_open", {"strategy": name, "perp": perp, "target_units": target,
                                     "approved_usd": verdict.approved_notional_usd, "filled": bool(fill),
                                     "rules": verdict.rules_fired})
        if fill is None or self._size(perp) == 0:
            return                                       # not filled: next pass
        del self.pending[name]
        if stop_px is not None and hasattr(self.adapter, "ledger") and self.adapter.ledger.stop_oid(perp) is None:
            self.notify(f"{name}: APERTO {perp} SENZA STOP SULL'EXCHANGE. Mettilo a mano o chiudi.")
            self.journal("follow_no_stop", {"strategy": name, "perp": perp})

    # ---- helpers -------------------------------------------------------------

    def _perp(self, name: str) -> str:
        return self.cfg.strumenti[self.cfg.strategie[name].strumento].perp

    def _target(self, name: str, w: Wanted, sz_decimals: int = 4) -> float:
        inst = self.cfg.strumenti[self.cfg.strategie[name].strumento]
        return round(w.micro * inst.unita_per_micro * self.cfg.scala, sz_decimals)

    def _size(self, perp: str) -> float:
        pos = self.adapter.account_state().position(perp)
        return pos.size if pos else 0.0

    def _once(self, name: str, key: str, text: str) -> None:
        if (name, key) not in self._said:
            self._said.add((name, key))
            self.notify(text)
