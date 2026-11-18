"""Il bridge a stato: il file di MultiCharts diventa la posizione su Hyperliquid (conto paper)."""
import pytest

from hlbridge.execution.paper import PaperAdapter
from hlbridge.follow.config import BridgeConfig
from hlbridge.follow.follower import Follower
from hlbridge.follow.stato import parse_line
from hlbridge.schemas import AssetContext

PERP = "xyz:XYZ100"
MID = 28_000.0


class FakeMarket:
    def __init__(self):
        self.mid = MID

    def contexts(self):
        return {PERP: AssetContext(asset=PERP, mark_px=self.mid, mid_px=self.mid, funding_hourly=0.0,
                                   open_interest=1e4, day_volume_usd=1e9, sz_decimals=4, max_leverage=30)}


class Spy(PaperAdapter):
    """Paper account that remembers the intents it was asked to carry out."""
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.intents = []

    def execute(self, intent, verdict, mid_px):
        self.intents.append(intent)
        return super().execute(intent, verdict, mid_px)


def cfg(**kw):
    d = dict(scala=0.05, tentativi=3,
             strumenti={"NQ": {"perp": PERP, "unita_per_micro": 2.0}},
             strategie={"DPB": {"file": "mario_stato_DPB.csv", "strumento": "NQ"}})
    d.update(kw)
    return BridgeConfig.model_validate(d)


@pytest.fixture
def env(tmp_path, limits, state):
    limits = dict(limits, max_notional_pct_equity={"crypto": 5.0, "hip3": 5.0}, max_gross_leverage=50.0,
                  max_net_beta_pct_equity=50.0)
    market = FakeMarket()
    adapter = Spy(starting_equity=100_000.0, fee_bps=0.0, slippage_bps=0.0, path=tmp_path / "paper.json")
    adapter.set_marks({PERP: MID})
    said, journal = [], []

    def build(config=None, **over):
        return Follower(config or cfg(), over.get("adapter", adapter), market, over.get("limits", limits), state,
                        tmp_path, journal=lambda k, p: journal.append((k, p)), notify=said.append)

    def write(text):
        (tmp_path / "mario_stato_DPB.csv").write_text(text)

    return type("E", (), dict(build=build, write=write, adapter=adapter, said=said, journal=journal,
                              market=market, limits=limits, state=state, dir=tmp_path))


def size(env):
    p = env.adapter.account_state().position(PERP)
    return p.size if p else 0.0


# ---- the file ------------------------------------------------------------------

def test_una_riga_completa_e_uno_stato_e_una_a_meta_no():
    assert parse_line("DPB;NQ;-1;120.00;FINE").micro == -1
    assert parse_line("DPB;NQ;1;120,5;FINE\r\n").stop_pts == 120.5
    assert parse_line("DPB;NQ;0;0;FINE").micro == 0
    for rotta in ("DPB;NQ;1;120", "DPB;NQ;1;120;FIN", "DPB;NQ;uno;120;FINE", "DPB;NQ;0.5;120;FINE", "", "DPB;NQ;1;-5;FINE"):
        assert parse_line(rotta) is None


# ---- l'avvio -------------------------------------------------------------------

def test_all_avvio_non_insegue_niente_e_lo_dice(env):
    env.write("DPB;NQ;-1;120.00;FINE")
    f = env.build()
    f.step()
    f.step()
    assert size(env) == 0 and env.adapter.intents == []
    assert any("Non inseguo" in s for s in env.said)


def test_all_avvio_concordi_non_dice_niente(env):
    env.write("DPB;NQ;0;0;FINE")
    env.build().step()
    assert env.said == []


# ---- i cambi -------------------------------------------------------------------

def test_un_cambio_apre_la_posizione_equivalente_con_il_suo_stop(env):
    env.write("DPB;NQ;0;0;FINE")
    f = env.build()
    f.step()
    env.write("DPB;NQ;-1;120.00;FINE")
    f.step()
    assert size(env) == pytest.approx(-0.1, rel=0.01)            # 1 micro x 2 unita x scala 0.05, short
    (intent,) = env.adapter.intents
    assert intent.side == "sell" and intent.stop_px == pytest.approx(MID + 120)
    assert intent.order_type == "limit_ioc" and intent.strategy_id == "DPB"


def test_il_cambio_di_lato_chiude_e_poi_apre(env):
    env.write("DPB;NQ;0;0;FINE")
    f = env.build()
    f.step()
    env.write("DPB;NQ;-1;120;FINE")
    f.step()
    env.write("DPB;NQ;1;120;FINE")
    f.step()
    assert size(env) == pytest.approx(0.1, rel=0.01)


def test_flat_chiude(env):
    env.write("DPB;NQ;0;0;FINE")
    f = env.build()
    f.step()
    env.write("DPB;NQ;1;120;FINE")
    f.step()
    env.write("DPB;NQ;0;0;FINE")
    f.step()
    assert size(env) == 0 and ("follow_close", {"strategy": "DPB", "perp": PERP, "filled": True}) in env.journal


def test_se_lo_stop_chiude_e_multicharts_non_cambia_non_riapre(env):
    env.write("DPB;NQ;0;0;FINE")
    f = env.build()
    f.step()
    env.write("DPB;NQ;1;120;FINE")
    f.step()
    env.adapter.close_position(PERP, "stop d'emergenza")      # scatta lo stop sull'exchange
    for _ in range(5):
        f.step()
    assert size(env) == 0


def test_un_cambio_di_size_dentro_un_trade_non_si_copia(env):
    env.write("DPB;NQ;0;0;FINE")
    f = env.build()
    f.step()
    env.write("DPB;NQ;1;120;FINE")
    f.step()
    env.write("DPB;NQ;2;120;FINE")
    f.step()
    assert size(env) == pytest.approx(0.1, rel=0.01)


def test_una_riga_a_meta_si_rilegge_al_giro_dopo(env):
    env.write("DPB;NQ;0;0;FINE")
    f = env.build()
    f.step()
    env.write("DPB;NQ;1;120")                                  # MultiCharts sta ancora scrivendo
    f.step()
    assert size(env) == 0
    env.write("DPB;NQ;1;120;FINE")
    f.step()
    assert size(env) == pytest.approx(0.1, rel=0.01)


def test_il_file_che_manca_non_e_uno_stato(env):
    f = env.build()
    f.step()
    assert env.adapter.intents == []


def test_un_file_di_un_altra_strategia_si_ignora_e_si_dice_una_volta(env):
    env.write("OBO;NQ;1;300;FINE")
    f = env.build()
    f.step(); f.step()
    assert size(env) == 0 and len([s for s in env.said if "lo ignoro" in s]) == 1


# ---- il rischio ----------------------------------------------------------------

def test_il_kill_switch_ferma_le_aperture_e_dopo_i_tentativi_si_ferma_e_avvisa(env):
    from hlbridge.risk.state import RiskState
    env.write("DPB;NQ;0;0;FINE")
    f = env.build()
    f.step()
    RiskState.engage_kill("test")
    env.write("DPB;NQ;1;120;FINE")
    for _ in range(6):
        f.step()
    assert size(env) == 0
    assert any("rischio rifiuta" in s for s in env.said) and any("Mi fermo" in s for s in env.said)
    assert "DPB" not in f.pending
    # il cambio successivo riparte da zero
    RiskState.release_kill()
    env.write("DPB;NQ;-1;120;FINE")
    f.step()
    assert size(env) == pytest.approx(-0.1, rel=0.01)


def test_una_chiusura_passa_anche_con_il_kill_switch(env):
    from hlbridge.risk.state import RiskState
    env.write("DPB;NQ;0;0;FINE")
    f = env.build()
    f.step()
    env.write("DPB;NQ;1;120;FINE")
    f.step()
    RiskState.engage_kill("test")
    env.write("DPB;NQ;0;0;FINE")
    f.step()
    assert size(env) == 0


def test_se_il_rischio_riduce_la_posizione_lo_dice(env, limits):
    env.write("DPB;NQ;0;0;FINE")
    stretti = dict(limits)                                      # il 2% dell'equity per un perp HIP-3
    f = env.build(limits=stretti)
    f.step()
    env.write("DPB;NQ;1;120;FINE")
    f.step()
    assert 0 < abs(size(env)) * MID <= 0.02 * 100_000 + 1
    assert any("riduce" in s for s in env.said)


def test_una_posizione_non_nostra_non_si_tocca(env):
    class Straniera(Spy):
        def account_state(self):
            st = super().account_state()
            return st.model_copy(update={"positions": [p.model_copy(update={"managed": False}) for p in st.positions]})

    a = Straniera(starting_equity=100_000.0, fee_bps=0.0, slippage_bps=0.0, path=env.dir / "x.json")
    a.set_marks({PERP: MID})
    from hlbridge.schemas import OrderIntent, RiskVerdict
    i = OrderIntent(asset=PERP, side="buy", notional_usd=1000, strategy_id="a mano", horizon_hours=0, reason="x")
    a.execute(i, RiskVerdict(intent_id=i.id, decision="approve", approved_notional_usd=1000), MID)
    env.write("DPB;NQ;0;0;FINE")
    f = env.build(adapter=a)
    f.step()
    before = a.account_state().position(PERP).size
    env.write("DPB;NQ;-1;120;FINE")
    f.step()
    assert a.account_state().position(PERP).size == before
    assert any("non è nostra" in s for s in env.said)


def test_se_lo_stop_non_e_sull_exchange_avvisa(env):
    class SenzaStop(Spy):
        class ledger:                                           # un ledger che non ha nessuno stop
            @staticmethod
            def stop_oid(asset):
                return None

    a = SenzaStop(starting_equity=100_000.0, fee_bps=0.0, slippage_bps=0.0, path=env.dir / "y.json")
    a.set_marks({PERP: MID})
    env.write("DPB;NQ;0;0;FINE")
    f = env.build(adapter=a)
    f.step()
    env.write("DPB;NQ;1;120;FINE")
    f.step()
    assert any("SENZA STOP" in s for s in env.said)


# ---- la config -----------------------------------------------------------------

def test_due_strategie_sullo_stesso_perp_sono_rifiutate():
    with pytest.raises(ValueError, match="subaccount"):
        cfg(strategie={"DPB": {"file": "a.csv", "strumento": "NQ"}, "OBO": {"file": "b.csv", "strumento": "NQ"}})


def test_uno_strumento_sconosciuto_e_rifiutato():
    with pytest.raises(ValueError, match="non è in"):
        cfg(strategie={"DPB": {"file": "a.csv", "strumento": "ES"}})


def test_la_config_vera_si_legge():
    from hlbridge.follow.config import load_bridge
    c = load_bridge()
    assert c.strumenti["NQ"].perp == PERP and c.strumenti["NQ"].unita_per_micro == 2.0


def test_una_perdita_oltre_il_limite_chiude_tutto_e_blocca(env):
    env.write("DPB;NQ;0;0;FINE")
    f = env.build()
    f.step()
    env.write("DPB;NQ;1;120;FINE")
    f.step()
    f.watch_risk()                                  # ancora il giorno comincia qui
    assert size(env) != 0
    env.state.day_start_equity = 200_000.0          # il conto e' a -50% sul giorno
    f.watch_risk()
    assert size(env) == 0 and env.state.halted and not env.state.flatten_requested
    assert any("Chiuse 1 posizioni del bridge (xyz:XYZ100)" in s for s in env.said)
    env.write("DPB;NQ;-1;120;FINE")                 # MultiCharts cambia: il rischio blocca l'apertura
    f.step()
    assert size(env) == 0


def test_i_limiti_del_bridge_stanno_sopra_quelli_del_desk():
    from hlbridge.follow.config import merge_limits
    m = merge_limits({"a": 1, "max_notional_pct_equity": {"crypto": 0.05, "hip3": 0.02}},
                     {"max_notional_pct_equity": {"hip3": 0.5}})
    assert m == {"a": 1, "max_notional_pct_equity": {"crypto": 0.05, "hip3": 0.5}}


def test_la_size_e_lo_stop_si_prezzano_dove_riposa_l_ordine(env):
    # sul testnet XYZ100 stava a 30.613 contro i 26.995 del mainnet: con il prezzo sbagliato lo stop di uno
    # short finiva sotto il mercato e scattava subito
    env.write("DPB;NQ;0;0;FINE")
    f = env.build()
    f.venue_mid = lambda perp: 30_000.0
    f.step()
    env.write("DPB;NQ;-1;120;FINE")
    f.step()
    (intent,) = env.adapter.intents
    assert intent.stop_px == pytest.approx(30_000.0 + 120)
    assert intent.limit_px == pytest.approx(30_000.0 * (1 - 0.002))     # lo scarto di default, 20 bps
    assert intent.notional_usd == pytest.approx(0.1 * intent.limit_px)  # le unita' sono quelle volute, qualunque sia il limite


def test_lo_slittamento_massimo_si_sceglie(env):
    env.write("DPB;NQ;0;0;FINE")
    f = env.build(cfg(slittamento_max_bps=1000))
    f.step()
    env.write("DPB;NQ;1;120;FINE")
    f.step()
    (intent,) = env.adapter.intents
    assert intent.limit_px == pytest.approx(MID * 1.10)
    assert size(env) == pytest.approx(0.1, rel=0.01)


def test_se_il_prezzo_di_esecuzione_manca_non_si_ordina_al_prezzo_del_mainnet(env):
    env.write("DPB;NQ;0;0;FINE")
    f = env.build()
    f.venue_mid = lambda perp: None
    f.step()
    env.write("DPB;NQ;-1;120;FINE")
    f.step()
    assert size(env) == 0 and env.adapter.intents == []
    assert any("non vedo il book" in s for s in env.said)


def test_il_limite_di_perdita_non_chiude_le_posizioni_che_non_sono_del_bridge(env):
    from hlbridge.schemas import OrderIntent, RiskVerdict
    i = OrderIntent(asset="BTC", side="buy", notional_usd=1000, strategy_id="a mano", horizon_hours=0, reason="x")
    env.adapter.execute(i, RiskVerdict(intent_id=i.id, decision="approve", approved_notional_usd=1000), 100.0)
    env.write("DPB;NQ;0;0;FINE")
    f = env.build()
    f.step()
    env.write("DPB;NQ;1;120;FINE")
    f.step()
    f.watch_risk()
    env.state.day_start_equity = 400_000.0
    f.watch_risk()
    assert size(env) == 0                                            # il perp del bridge e' chiuso
    btc = env.adapter.account_state().position("BTC")
    assert btc is not None and btc.size != 0                         # l'altra posizione no
