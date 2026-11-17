"""config/bridge.yaml: quali strategie seguire, su quale perp, in che misura."""
from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field, model_validator

from hlbridge.config import ROOT

BRIDGE_PATH = ROOT / "config" / "bridge.yaml"


class Instrument(BaseModel):
    perp: str                                   # 'xyz:XYZ100'
    unita_per_micro: float = Field(gt=0)        # unità di perp per 1 micro: $ al punto del micro / $ al punto di 1 unità


class StrategyCfg(BaseModel):
    file: str                                   # mario_stato_<STRAT>.csv, dentro cartella_stati
    strumento: str                              # una chiave di `strumenti`


class BridgeConfig(BaseModel):
    cartella_stati: str | None = None           # dove MultiCharts scrive i file; oppure $BRIDGE_STATE_DIR
    scala: float = Field(gt=0, le=1.0)          # frazione della size di MultiCharts: 1.0 = una a una
    tentativi: int = Field(default=5, ge=1)     # per cambio di posizione, poi si ferma fino al cambio successivo
    strumenti: dict[str, Instrument]
    strategie: dict[str, StrategyCfg]
    limiti: dict = Field(default_factory=dict)  # sopra config/limits.yaml, chiave per chiave: i limiti di questo bridge

    @model_validator(mode="after")
    def _check(self):
        seen: dict[str, str] = {}
        for name, s in self.strategie.items():
            if s.strumento not in self.strumenti:
                raise ValueError(f"{name}: strumento {s.strumento!r} non è in `strumenti`")
            perp = self.strumenti[s.strumento].perp
            if perp in seen:
                raise ValueError(
                    f"{seen[perp]} e {name} vogliono lo stesso perp {perp}: su un conto solo Hyperliquid "
                    "tiene una posizione netta per perp, e due strategie si pesterebbero. "
                    "Serve un subaccount per strategia (ancora non c'è).")
            seen[perp] = name
        return self


def load_bridge(path: Path = BRIDGE_PATH) -> BridgeConfig:
    return BridgeConfig.model_validate(yaml.safe_load(Path(path).read_text()))


def merge_limits(base: dict, over: dict) -> dict:
    """limits.yaml with the bridge's own numbers on top, nested keys merged one by one."""
    out = dict(base)
    for k, v in over.items():
        out[k] = merge_limits(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out
