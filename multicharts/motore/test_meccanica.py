"""PYTHONPATH=multicharts python3 -m unittest motore.test_meccanica -v"""
import contextlib, datetime as dt, io, unittest

from .meccanica import del_giorno, meccanica, stampa
from .motore import Trade


def trade(t_in, t_out, p_in, p_out, nome_out, lato=1):
    t = Trade(lato, 1, t_in, p_in, 'X.L')
    t.t_out, t.p_out, t.nome_out = t_out, p_out, nome_out
    return t


DOM = dt.datetime(2020, 1, 5, 19, 1)
TRADE = [trade(DOM, dt.datetime(2020, 1, 6, 15, 56), 3217.25, 3243.75, 'L.Flat'),
         trade(DOM + dt.timedelta(days=7), dt.datetime(2020, 1, 13, 9, 12), 3271.5, 3371.5, 'L.TP'),
         trade(DOM + dt.timedelta(days=14), dt.datetime(2020, 1, 20, 3, 40), 3318.75, 3228.75, 'L.SL')]


class Meccanica(unittest.TestCase):
    def test_conta_giorni_e_orari(self):
        m = meccanica(TRADE, 12)
        self.assertEqual(m['trade'], 3)
        self.assertEqual(m['ingressi_per_giorno_della_settimana'], {'dom': 3})
        self.assertEqual((m['ingresso_primo'], m['ingresso_ultimo']), ('19:01', '19:01'))
        self.assertEqual(m['uscite_giorni_della_settimana'], ['lun'])
        self.assertEqual((m['uscita_prima'], m['uscita_ultima']), ('03:40', '15:56'))
        self.assertEqual(m['a_cavallo_di_due_date'], 3)
        self.assertEqual(m['massimo_in_un_giorno'], 1)

    def test_non_esce_niente_che_dica_se_guadagna(self):
        # Ne' un prezzo, ne' i punti, ne' quante uscite ha ogni segnale (sarebbe un win rate).
        m = meccanica(TRADE, 12)
        self.assertEqual(m['segnali_di_uscita'], ['L.Flat', 'L.SL', 'L.TP'])
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            stampa(m)
        testo = out.getvalue() + repr(m) + repr(del_giorno(TRADE, dt.date(2020, 1, 13)))
        for vietato in ('3217', '3243', '3271', '3371', '3318', '3228', '26.5', '100.0', '-90', '$', 'L.TP (', 'L.SL ('):
            self.assertNotIn(vietato, testo)

    def test_il_giorno_elenca_solo_segnale_d_ingresso_e_orari(self):
        righe = del_giorno(TRADE, dt.date(2020, 1, 13))
        self.assertEqual(righe, [('X.L', 'long', '2020-01-12 19:01:00', '2020-01-13 09:12:00')])

    def test_zero_trade_si_dice(self):
        self.assertEqual(meccanica([], 12), {'trade': 0, 'giorni_di_mercato': 12})


if __name__ == '__main__':
    unittest.main()
