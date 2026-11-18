"""Il file di stato di MultiCharts: quello che la strategia vuole, una riga.

    DPB;NQ;-1;120.00;FINE

strategia ; strumento ; posizione voluta in micro (negativa = short, 0 = flat) ; stop d'emergenza
in punti ; FINE. È il formato del bridge a stato di multicharts/bridge/SPEC.md, lo stesso che
legge l'EA di MT5. Una riga senza FINE, o un file che manca mentre MultiCharts lo riscrive, non
è uno stato: si rilegge al giro dopo.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Wanted:
    strategy: str
    instrument: str
    micro: int            # signed: + long, - short, 0 flat
    stop_pts: float       # emergency stop distance, in index points


def parse_line(text: str) -> Wanted | None:
    """None when the line is not a complete state: torn write, wrong shape, not a number."""
    parts = [p.strip() for p in text.strip().lstrip("\ufeff").split(";")]
    if len(parts) != 5 or parts[4] != "FINE" or not parts[0] or not parts[1]:
        return None
    try:
        micro = float(parts[2].replace(",", "."))
        stop = float(parts[3].replace(",", "."))
    except ValueError:
        return None
    if micro != int(micro) or stop < 0:
        return None                       # half a micro does not exist; a negative stop is a garbled line
    return Wanted(parts[0], parts[1], int(micro), stop)


def read_state(path: Path) -> Wanted | None:
    """The state in the file, or None when there is none to read right now."""
    try:
        lines = [l for l in path.read_text(errors="replace").splitlines() if l.strip()]
    except OSError:
        return None
    return parse_line(lines[-1]) if lines else None


def diagnose(path: Path) -> str:
    """Why `read_state` found nothing, in words for an alert."""
    if not path.parent.exists():
        return f"la cartella {path.parent} non esiste"
    if not path.exists():
        return "il file non c'è"
    try:
        lines = [l for l in path.read_text(errors="replace").splitlines() if l.strip()]
    except OSError as e:
        return f"non si apre ({e.__class__.__name__})"
    if not lines:
        return "il file è vuoto"
    return f"l'ultima riga non è nel formato (STRAT;STRUM;POS;STOP;FINE): {lines[-1][:60]!r}"
