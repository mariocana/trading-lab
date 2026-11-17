"""Il muro sulle fonti: cosa c'è in idee/<id>/fonti/ prima che un agente la legga.

Ricercatore, critico e coder non devono vedere una nostra misura, un report o un verdetto. Le
fonti però possono portare numeri: quello che un paper o un autore DICHIARA è materia del
critico. Un controllo automatico non sa distinguere le due cose da un numero, quindi divide in
due:

- `nostre`: righe che parlano di una misura fatta da noi (il desk, il lab, un nostro run, un
  report, un verdetto). Vanno tolte: con una riga così `ricerca fonti` rifiuta.
- `numeri`: righe con un numero di performance senza quei segni. Il desk le legge una per una
  e controlla che siano dichiarazioni della fonte.

È un setaccio largo, non una prova: una riga pulita qui può ancora dire troppo.
"""
from __future__ import annotations

import re
from pathlib import Path

TESTO = {".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".el", ".py"}

NOSTRE = re.compile(
    r"contaminazion|il desk ha|misura del desk|misurat[oa] dal desk|abbiamo (misurat|girat|guardat|vist)"
    r"|nostr[oa] (run|misura|backtest|report)|gi[aà] (misurat|girat|guardat)|misura\.json|dossier\.md"
    r"|reports?/|verdett|verdict|pipeline_status|cimitero|causa di morte|gate \d (fallit|passat)"
    r"|motore\.misura|check_report|sopra soglia|sotto soglia",
    re.IGNORECASE)

NUMERI = re.compile(
    r"\bt\s*(=|:|di|della media)?\s*[−+-]?\d+[.,]\d+"          # t 2,51
    r"|\b(wr|win rate|pf|profit factor|sharpe|sortino|avg|average trade|media per trade|drawdown|dd)\b[^|\n]{0,40}\d"
    r"|\d[^|\n]{0,12}\b(wr|win rate|pf|profit factor|sharpe)\b"
    r"|\$\s?[\d.,]+\s*(per|a|al)\s*(trade|micro|contratto|giorno)"
    r"|\b\d{2,}[\d.]*\s+trade\b"
    r"|\beccesso\b[^|\n]{0,30}\d|\berrori standard\b[^|\n]{0,20}\d",
    re.IGNORECASE)


def scan(cartella: Path) -> tuple[list[tuple[str, int, str]], list[tuple[str, int, str]], list[str]]:
    """(nostre, numeri, non_letti): righe come (file, numero di riga, testo)."""
    nostre, numeri, non_letti = [], [], []
    for f in sorted(p for p in cartella.rglob("*") if p.is_file()):
        nome = str(f.relative_to(cartella))
        if f.suffix.lower() not in TESTO:
            non_letti.append(nome)
            continue
        for i, riga in enumerate(f.read_text(errors="replace").splitlines(), 1):
            if riga.lstrip().startswith(">"):       # le note del desk in cima alla fonte
                continue
            if NOSTRE.search(riga):
                nostre.append((nome, i, riga.strip()))
            elif NUMERI.search(riga):
                numeri.append((nome, i, riga.strip()))
    return nostre, numeri, non_letti
