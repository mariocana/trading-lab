"""prova2_orb_breakout (ricerca/idee/prova2_orb_breakout/hypothesis.md, «Regola eseguibile»).

Una serie: barre da 5 minuti di NQ, ora di Chicago, etichetta = ora di chiusura.
Range = barre che chiudono dalle 08:35 alle 09:00 (senza la barra delle 08:35 il giorno si salta).
Setup = prima barra fra le 09:05 e le 13:50 con chiusura > massimo del range; solo long, un setup
al giorno. Ingresso a mercato alla barra dopo, stop al minimo del range, target ingresso + 1R,
uscita a mercato dopo la barra delle 14:00.

Come il motore lo esegue (scelte di esecuzione, la regola non cambia):
- lo stop parte insieme all'ingresso (attivo gia' nella barra del fill, come `OBO-L-SL0`); il
  target dipende dal fill, quindi parte dalla chiusura della barra d'ingresso;
- l'uscita «alla chiusura della barra delle 14:00» e' un ordine a mercato all'apertura della
  barra dopo (14:00:00), perche' il motore non esegue alla chiusura della barra corrente;
- stop e target nello stesso minuto: decide il percorso del Bar Magnifier, non «prima lo stop»;
- R <= 0 (apertura della barra d'ingresso al minimo del range o sotto): il motore compra comunque
  e lo stop chiude subito all'apertura del minuto; il giorno e' chiuso come vuole la regola;
- sessioni accorciate: flat con `SetExitOnClose` del motore all'ultima barra della sessione.
"""

DEFAULT = dict(RangeStart=835, RangeEnd=900, SetupStart=905, SetupEnd=1350, FlatTime=1400,
               TargetR=1.0, NumContracts=1)


class ORBBreakout:
    def __init__(self, **inp):
        self.p = dict(DEFAULT, **inp)
        self.dataPrec = None
        self.orHigh, self.orLow = 0.0, 999999.0
        self.giornoOK = False             # c'e' la barra delle 08:35
        self.fatto = False                # primo setup del giorno gia' preso

    def su_barra(self, ctx):
        p, b = self.p, ctx.b()
        t = b.ora

        if b.data != self.dataPrec:
            self.orHigh, self.orLow = 0.0, 999999.0
            self.giornoOK = self.fatto = False
            self.dataPrec = b.data

        if t == p['RangeStart']:
            self.giornoOK = True
        if self.giornoOK and p['RangeStart'] <= t <= p['RangeEnd']:
            self.orHigh = max(self.orHigh, b.h)
            self.orLow = min(self.orLow, b.l)

        mp = ctx.market_position
        if mp == 0 and self.giornoOK and not self.fatto and p['SetupStart'] <= t <= p['SetupEnd'] \
                and b.c > self.orHigh:
            self.fatto = True
            ctx.buy('ORB.L', p['NumContracts'])
            ctx.sell('ORB.L.SL', self.orLow, 'stop')

        if mp == 1:
            if t >= p['FlatTime']:
                ctx.sell('ORB.L.Flat')
            else:
                r = ctx.entry_price - self.orLow
                ctx.sell('ORB.L.SL', self.orLow, 'stop')
                ctx.sell('ORB.L.TP', ctx.entry_price + p['TargetR'] * r, 'limite')
