"""I comandi rifiutano quello che il processo vieta."""
import json

import pytest

import ricerca.cli as cli
import ricerca.registry as reg
from ricerca.perimetro import load_perimeter


@pytest.fixture
def lab(tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "IDEE", tmp_path / "idee")
    monkeypatch.setattr(reg, "REGISTRY_PATH", tmp_path / "trials.jsonl")
    return tmp_path


def args(**kw):
    class A:
        pass
    a = A()
    a.id, a.title, a.door, a.parent, a.step, a.reason = "fine_mese", "Flussi di fine mese", "user", None, None, None
    a.horizon, a.market, a.destination = "intraday", "NQ", "prop"
    for k, v in kw.items():
        setattr(a, k, v)
    return a


BUONA = {"errori_standard": 3.4, "dollari_al_giorno_per_micro": 15.0}


def test_un_idea_ha_una_cartella_e_una_riga_nel_registro(lab):
    cli.cmd_idea(args())
    assert (lab / "idee" / "fine_mese" / "hypothesis.md").exists()
    assert reg.Registry().ideas() == ["fine_mese"]
    with pytest.raises(SystemExit, match="esiste già"):
        cli.cmd_idea(args())


def test_un_idea_fuori_perimetro_non_viene_registrata(lab):
    for kw in ({"horizon": "daily"}, {"horizon": "swing"}, {"horizon": "scalping"}, {"market": "GC"}, {"market": "YM"},
               {"destination": "swing"}):
        with pytest.raises(SystemExit, match="fuori dal perimetro"):
            cli.cmd_idea(args(**kw))
    assert reg.Registry().ideas() == [] and not (lab / "idee" / "fine_mese").exists()


def test_un_orizzonte_acceso_senza_misura_resta_chiuso():
    per = load_perimeter()
    acceso = per.model_copy(deep=True)
    acceso.orizzonti["daily"].attivo = True
    assert any("senza una misura" in x for x in acceso.check_idea("daily", "NQ"))
    acceso.orizzonti["daily"].misura = "giornaliera"
    assert acceso.check_idea("daily", "NQ") == []


def test_una_misura_si_registra_dal_suo_file_e_si_conta(lab):
    cli.cmd_idea(args())
    with pytest.raises(SystemExit, match="misura.json"):
        cli.cmd_measure(args())
    (lab / "idee" / "fine_mese" / "misura.json").write_text(json.dumps(BUONA))
    cli.cmd_measure(args())
    assert reg.Registry().ideas_measured() == 1


def test_il_tetto_mensile_ferma_le_idee_nuove_ma_non_un_rilancio(lab):
    cap = load_perimeter().misura.idee_al_mese_max
    for i in range(cap + 1):
        a = args(id=f"idea_{i}")
        cli.cmd_idea(a)
        (lab / "idee" / a.id / "misura.json").write_text(json.dumps(BUONA))
        if i < cap:
            cli.cmd_measure(a)
    with pytest.raises(SystemExit, match="tetto mensile"):
        cli.cmd_measure(args(id=f"idea_{cap}"))
    cli.cmd_measure(args(id="idea_0"))                 # già misurata: un rilancio, non uno sguardo nuovo


def test_i_minimi_sono_gli_stessi_per_ogni_idea_della_stessa_destinazione(lab, capsys):
    cli.cmd_idea(args())
    f = lab / "idee" / "fine_mese" / "misura.json"
    f.write_text(json.dumps(BUONA))
    cli.cmd_measure(args())
    assert "SOPRA SOGLIA" in capsys.readouterr().out
    f.write_text(json.dumps({"errori_standard": 0.45, "dollari_al_giorno_per_micro": 2.0}))
    cli.cmd_measure(args())
    assert "SOTTO SOGLIA" in capsys.readouterr().out


def test_un_idea_uccisa_e_chiusa_per_sempre(lab, capsys):
    cli.cmd_idea(args())
    cli.cmd_kill(args(step="critic", reason="nessuno che perde"))
    assert (lab / "idee" / "fine_mese" / "KILLED").read_text().startswith("critic")
    with pytest.raises(reg.RegistryError):
        cli.cmd_kill(args(step="user", reason="di nuovo"))
    cli.cmd_status(args())
    assert "uccisa (critic)" in capsys.readouterr().out


POCHI_DOLLARI = {"errori_standard": 3.4, "dollari_al_giorno_per_micro": 4.0, "media_per_trade": 250.0}


def test_la_destinazione_decide_i_minimi(lab, capsys):
    cli.cmd_idea(args(id="da_prop"))
    cli.cmd_idea(args(id="da_live", destination="live"))
    for i in ("da_prop", "da_live"):
        (lab / "idee" / i / "misura.json").write_text(json.dumps(POCHI_DOLLARI))
    cli.cmd_measure(args(id="da_prop"))
    out = capsys.readouterr().out
    assert "destinazione prop: SOTTO SOGLIA" in out and "$ al giorno per micro" in out
    cli.cmd_measure(args(id="da_live"))
    out = capsys.readouterr().out
    assert "destinazione live: SOPRA SOGLIA" in out
    assert "da guardare, non uccide: media per trade $25.00 per micro" in out


def test_il_live_non_abbassa_gli_errori_standard(lab, capsys):
    cli.cmd_idea(args(destination="live"))
    (lab / "idee" / "fine_mese" / "misura.json").write_text(
        json.dumps({"errori_standard": 2.75, "dollari_al_giorno_per_micro": 4.98, "media_per_trade": 279.79}))
    cli.cmd_measure(args())
    assert "destinazione live: SOTTO SOGLIA: errori standard 2.75 < 3.0" in capsys.readouterr().out


def test_un_idea_nata_prima_delle_destinazioni_e_prop(lab, capsys):
    reg.Registry().register_idea("vecchia", "Senza destinazione", "user", horizon="intraday", market="NQ")
    (lab / "idee" / "vecchia").mkdir(parents=True)
    (lab / "idee" / "vecchia" / "misura.json").write_text(json.dumps(POCHI_DOLLARI))
    cli.cmd_measure(args(id="vecchia"))
    assert "destinazione prop: SOTTO SOGLIA" in capsys.readouterr().out


def test_le_fonti_con_una_nostra_misura_non_passano(lab, capsys):
    cli.cmd_idea(args())
    d = lab / "idee" / "fine_mese" / "fonti"
    d.mkdir()
    (d / "idea.md").write_text(
        "> nota del desk: la misura del desk e stata tolta\n"
        "# Idea\nL'autore dichiara 823 trade, WR 58%, PF 1.28.\nMax 1 trade al giorno, stop 90 punti.\n")
    (d / "paper.pdf").write_bytes(b"%PDF")
    cli.cmd_fonti(args())
    out = capsys.readouterr().out
    assert "idea.md:3" in out and "paper.pdf" in out and "nessuna nostra misura" in out
    assert "idea.md:4" not in out and "idea.md:1" not in out       # una regola e una nota del desk non sono numeri
    (d / "idea.md").write_text("## Contaminazione\nIl desk ha già misurato l'IS: 257 lunedì, t 2,51.\n")
    with pytest.raises(SystemExit, match="non pulite"):
        cli.cmd_fonti(args())
    assert "idea.md:2" in capsys.readouterr().out
