"""monday_long (ricerca/idee/monday_long/hypothesis.md, «Regola eseguibile»).

Long ES dalla chiusura del minuto 19:00 CT di domenica alla chiusura del minuto 15:55 CT di lunedi',
stop 90 punti, target 100. Una serie: barre da 1 minuto (ognuna ha dentro se stessa per il Bar
Magnifier). La sessione Globex e' quella del lunedi' (17:00 di domenica -> 16:00 di lunedi'): il
trade cambia data ma non sessione, e il motore lo chiude a fine sessione solo alla pausa dopo le
16:00 del lunedi'.

- Ingresso: alla chiusura del minuto timbrato 19:00 di domenica, a mercato -> fill all'apertura
  del minuto 19:01. Se il minuto 19:00 manca, quel lunedi' non si trada.
- Stop e target dalla chiusura della barra d'ingresso: attivi dal minuto 19:02.
- Uscita a tempo: alla chiusura del primo minuto del lunedi' con ora fra 15:55 e 16:00 -> fill
  all'apertura del minuto dopo. Rete finale: esci_a_chiusura del motore alle 16:00.
- Lunedi' esclusi (festivi NYSE e chiusure anticipate alle 13:00 ET) calcolati per regola.
"""
import datetime as dt

DEFAULT = dict(EntryTime=1900, ExitTime=1555, SessEnd=1600, StopPts=90, TargetPts=100, NumContracts=1)


def _n_esimo_lunedi(anno, mese, n):
    d = dt.date(anno, mese, 1)
    d += dt.timedelta(days=(0 - d.weekday()) % 7)
    return d + dt.timedelta(weeks=n - 1)


def _ultimo_lunedi(anno, mese):
    d = dt.date(anno + (mese == 12), mese % 12 + 1, 1) - dt.timedelta(days=1)
    return d - dt.timedelta(days=d.weekday())


def _osservato_di_lunedi(d):
    """Il lunedi' in cui cade o si osserva la festa fissa d (se cade di domenica), altrimenti None.
    Se cade di sabato non si osserva di lunedi'."""
    if d.weekday() == 0:
        return d
    if d.weekday() == 6:
        return d + dt.timedelta(days=1)
    return None


def lunedi_esclusi(anno):
    """Lunedi' di quell'anno con la NYSE chiusa o a chiusura anticipata (13:00 ET)."""
    ex = {_n_esimo_lunedi(anno, 1, 3),           # Martin Luther King
          _n_esimo_lunedi(anno, 2, 3),           # Presidents' Day
          _ultimo_lunedi(anno, 5),               # Memorial Day
          _n_esimo_lunedi(anno, 9, 1)}           # Labor Day
    fisse = [dt.date(anno, 1, 1), dt.date(anno, 7, 4), dt.date(anno, 12, 25)]
    if anno >= 2022:
        fisse.append(dt.date(anno, 6, 19))       # Juneteenth
    for d in fisse:
        l = _osservato_di_lunedi(d)
        if l is not None:
            ex.add(l)
    for d in (dt.date(anno, 7, 3), dt.date(anno, 12, 24)):   # chiusure anticipate, solo se lunedi'
        if d.weekday() == 0:
            ex.add(d)
    return ex


class MondayLong:
    def __init__(self, **inp):
        self.p = dict(DEFAULT, **inp)
        self._esclusi = {}
        self.sessione_tradata = None             # lunedi' della sessione gia' tradata

    def escluso(self, lunedi):
        if lunedi.year not in self._esclusi:
            self._esclusi[lunedi.year] = lunedi_esclusi(lunedi.year)
        return lunedi in self._esclusi[lunedi.year]

    def su_barra(self, ctx):
        p, b = self.p, ctx.b()
        mp = ctx.market_position

        # ingresso: minuto 19:00 di domenica, sessione del lunedi' dopo
        if mp == 0 and b.ora == p['EntryTime'] and b.data.weekday() == 6:
            lunedi = b.data + dt.timedelta(days=1)
            if lunedi != self.sessione_tradata and not self.escluso(lunedi):
                ctx.buy('ML.L', p['NumContracts'])
                self.sessione_tradata = lunedi

        if mp == 1:
            ctx.sell('L.SL', ctx.entry_price - p['StopPts'], 'stop')
            ctx.sell('L.TP', ctx.entry_price + p['TargetPts'], 'limite')
            # uscita a tempo: solo il lunedi', dalle 15:55 (o dal primo minuto dopo, se manca)
            if b.data.weekday() == 0 and p['ExitTime'] <= b.ora <= p['SessEnd']:
                ctx.sell('L.Flat')
