"""Registro delle strategie del motore: serie, simbolo, valore del punto, costi del report MC."""
from .dpb import DPB
from .obo import OBO
from .prova_nq_first5 import PROVA_NQ_FIRST5
from .prova2_last_half_hour import PROVA2_LAST_HALF_HOUR
from .prova_vwap_fade import VwapFade
from .prova2_orb_breakout import ORBBreakout
from .monday_long import MondayLong

STRATEGIE = {
    'dpb': dict(classe=DPB, simbolo='NQ', tf=(5, 15), punto=20.0, comm_lato=7.5, riscaldamento=10),
    'obo': dict(classe=OBO, simbolo='NQ', tf=(15,), punto=20.0, comm_lato=7.5, riscaldamento=60),
    'prova_nq_first5': dict(classe=PROVA_NQ_FIRST5, simbolo='NQ', tf=(5,), punto=20.0, comm_lato=7.5,
                            riscaldamento=5),
    'prova2_last_half_hour': dict(classe=PROVA2_LAST_HALF_HOUR, simbolo='NQ', tf=(5,), punto=20.0,
                                  comm_lato=7.5, riscaldamento=5),
    'prova_vwap_fade': dict(classe=VwapFade, simbolo='NQ', tf=(5, 1), punto=20.0, comm_lato=7.5,
                            riscaldamento=3),
    'prova2_orb_breakout': dict(classe=ORBBreakout, simbolo='NQ', tf=(5,), punto=20.0, comm_lato=7.5,
                                riscaldamento=3),
    'monday_long': dict(classe=MondayLong, simbolo='ES', tf=(1,), punto=50.0, comm_lato=15.0,
                        riscaldamento=3),
}
