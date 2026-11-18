"""hlbridge <command>

  status [--live]   equity, positions, risk state, kill switch
  follow [--live]   il bridge: legge i file di stato di MultiCharts e copia la posizione su Hyperliquid
                    (config/bridge.yaml). Senza --live è un conto paper a prezzi veri
  kill / unkill     engage / release the kill switch (file in var/)
  unlock            clear a drawdown / daily-loss halt
  journal [--kind K] [--last N]
  ui [--port 8765] [--reload]
                    start the web UI (the normal way to run the bridge).
                    Compiles every module and parses the dashboard script first.
"""
from __future__ import annotations

import argparse
import json
import logging
import sys

from hlbridge.config import load_limits, settings
from hlbridge.data.hl_market import HLMarket
from hlbridge.risk.state import RiskState, state_path


def _market() -> HLMarket:
    return HLMarket(settings().data_url, settings().dexs)


def _risk_state(live: bool) -> RiskState:
    s = settings()
    return RiskState.load(state_path("live" if live else "paper", s.account_address))


def _adapter(live: bool):
    if not live:
        from hlbridge.execution.paper import PaperAdapter
        return PaperAdapter()
    s = settings()
    if not (s.account_address and s.api_wallet_key):
        sys.exit("--live needs HL_ACCOUNT_ADDRESS and HL_API_WALLET_KEY in .env")
    if not s.testnet:
        print("!! MAINNET. Type MAINNET to continue: ", end="", flush=True)
        if input().strip() != "MAINNET":
            sys.exit("aborted")
    from hlbridge.execution.hyperliquid import HyperliquidAdapter
    return HyperliquidAdapter(s.base_url, s.account_address, s.api_wallet_key, s.unified_collateral, s.dexs)


def cmd_status(args):
    adapter = _adapter(args.live)
    if hasattr(adapter, "set_marks"):
        adapter.set_marks({a: c.mid_px for a, c in _market().contexts().items()})
    acc = adapter.account_state()
    st = _risk_state(args.live)
    print(f"adapter      {adapter.name}   exec: {'testnet' if settings().testnet else 'MAINNET'}   data: mainnet")
    print(f"equity       {acc.equity_usd:,.2f}   gross {acc.gross_notional_usd:,.2f}   day {st.day_pnl_pct(acc.equity_usd):+.2%}")
    print(f"peak         {st.peak_equity:,.2f}   halted={st.halted} {st.halt_reason}   kill={RiskState.kill_engaged()}")
    for p in acc.positions:
        print(f"  {p.asset:<12} {p.notional_usd:>12,.2f}  entry {p.entry_px:<12g} mark {p.mark_px:<12g} upnl {p.unrealized_pnl_usd:>9,.2f}  {p.strategy_id or ''}")


def cmd_follow(args):
    import os
    import time

    from hlbridge.follow.config import exposure_lines, load_bridge, merge_limits
    from hlbridge.follow.follower import Follower
    from hlbridge.pm.notify import notify

    cfg = load_bridge()
    folder = cfg.cartella_stati or os.environ.get("BRIDGE_STATE_DIR")
    if not folder:
        sys.exit("manca la cartella dei file di stato: cartella_stati in config/bridge.yaml o BRIDGE_STATE_DIR")
    adapter, market, st = _adapter(args.live), _market(), _risk_state(args.live)
    def venue_mid(perp):                                    # where the order rests, not the mainnet feed
        try:
            return adapter.venue.book_depth_10bps(perp)[0]
        except Exception:                                   # noqa: BLE001
            return None
    limits = merge_limits(load_limits(), cfg.limiti)
    f = Follower(cfg, adapter, market, limits, st, folder, venue_mid=venue_mid if args.live else None)
    try:                                                    # what one micro weighs against the cap: say it before it cuts
        ctxs = market.contexts()
        prices = {p: (venue_mid(p) if args.live else None) or ctxs[p].mid_px for p in {i.perp for i in cfg.strumenti.values()} if p in ctxs}
        for line in exposure_lines(cfg, limits, adapter.account_state().equity_usd, prices):
            print(line)
    except Exception as e:                                  # noqa: BLE001 - a start-up note must not stop the bridge
        print(f"(non ho potuto calcolare quanto pesa un micro: {e!r})")
    print(f"bridge: {', '.join(cfg.strategie)} da {folder}, scala {cfg.scala}, "
          f"{'LIVE ' + ('testnet' if settings().testnet else 'MAINNET') if args.live else 'paper'}")
    last_marks = last_risk = 0.0
    told = set()
    while True:
        now = time.time()
        try:
            if not args.live and now - last_marks > 5:          # the paper account marks at real prices
                adapter.set_marks({a: c.mid_px for a, c in market.contexts().items()})
                last_marks = now
            f.step()
            if now - last_risk > 60:
                f.watch_risk()
                last_risk = now
        except Exception as e:                                  # noqa: BLE001 - a bridge that dies on one bad read stops following
            logging.getLogger("hlbridge.follow").exception("passo fallito")
            if repr(e) not in told:
                told.add(repr(e))
                notify(f"Il bridge ha un errore e continua a girare: {e!r}")
        if args.once:
            return
        time.sleep(args.interval)


def cmd_kill(args):
    RiskState.engage_kill("cli")
    print("kill switch ENGAGED: no new risk will be taken. Closing is still allowed.")


def cmd_unkill(args):
    RiskState.release_kill()
    print("kill switch released")


def cmd_unlock(args):
    st = _risk_state(getattr(args, "live", False))
    print(f"was: halted={st.halted} {st.halt_reason}")
    st.unlock()
    st.save()
    print("unlocked")


def cmd_journal(args):
    from hlbridge.journal.log import read
    rows = read(kind=args.kind)[-args.last:]
    for r in rows:
        print(json.dumps(r))


def cmd_ui(args):
    from hlbridge.ui.server import main as serve
    serve(host=args.host, port=args.port, reload=args.reload, skip_preflight=args.no_preflight)


def main(argv=None):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    p = argparse.ArgumentParser(prog="hlbridge", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status"); s.add_argument("--live", action="store_true"); s.set_defaults(fn=cmd_status)
    fo = sub.add_parser("follow")
    fo.add_argument("--live", action="store_true", help="ordini veri (testnet salvo HL_TESTNET=0); senza, conto paper")
    fo.add_argument("--interval", type=float, default=1.0, help="secondi fra due letture dei file (default 1)")
    fo.add_argument("--once", action="store_true", help="un solo passo, per provare")
    fo.set_defaults(fn=cmd_follow)
    sub.add_parser("kill").set_defaults(fn=cmd_kill)
    sub.add_parser("unkill").set_defaults(fn=cmd_unkill)
    ul = sub.add_parser("unlock"); ul.add_argument("--live", action="store_true"); ul.set_defaults(fn=cmd_unlock)
    j = sub.add_parser("journal"); j.add_argument("--kind"); j.add_argument("--last", type=int, default=20)
    j.set_defaults(fn=cmd_journal)
    u = sub.add_parser("ui")
    u.add_argument("--port", type=int, default=None, help="default 8765, or $PORT")
    u.add_argument("--host", default=None, help="default 127.0.0.1, or $HOST. Anything else needs DESK_PASSWORD")
    u.add_argument("--reload", action="store_true", help="restart the desk when a source file changes (development only)")
    u.add_argument("--no-preflight", action="store_true", help="skip the compile/parse check before starting")
    u.set_defaults(fn=cmd_ui)

    args = p.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
