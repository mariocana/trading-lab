"""prova2_last_half_hour (ricerca/idee/prova2_last_half_hour/hypothesis.md, «Regola eseguibile»).

Una serie: barre da 5 minuti di NQ, etichetta all'ora di chiusura (la barra delle 14:30 copre
14:25-14:30). Riferimento = close della barra delle 15:00 dell'ultima sessione precedente che ha
quella barra. Alla chiusura della barra delle 14:30: r_ROD = Close / riferimento - 1; LONG se
r_ROD > 0, SHORT se r_ROD <= 0. Uscita a mercato alla chiusura della barra delle 15:00. Un trade
al giorno, nessuno stop, nessun target.

Il motore conosce solo ordini per la barra dopo: ingresso e uscita «a mercato» decisi alla
chiusura delle barre 14:30 e 15:00 scattano all'apertura della barra successiva (14:30:00 e
15:00:00, lo stesso istante a pochi tick di distanza).

Giorni senza barra delle 14:30 (chiusure anticipate, buchi): nessun trade, da soli. Una sessione
con la barra delle 14:30 ma senza quella delle 15:00 non si puo' sapere alle 14:30 senza guardare
avanti: se capita, l'uscita e' alla chiusura della prima barra con orario >= 15:00, o il
SetExitOnClose del motore. Nel 2020-2024 non capita.
"""

DEFAULT = dict(EntryTime=1430, ExitTime=1500, MaxTradesPerDay=1, NumContracts=1)


class PROVA2_LAST_HALF_HOUR:
    def __init__(self, **inp):
        self.p = dict(DEFAULT, **inp)
        self.rif = None               # close della barra delle 15:00 dell'ultima sessione che l'ha
        self.dataPrec = None
        self.tradesToday = 0

    def su_barra(self, ctx):
        p, b = self.p, ctx.b()

        if b.data != self.dataPrec:
            self.tradesToday = 0
        self.dataPrec = b.data

        mp = ctx.market_position
        if mp == 0 and b.ora == p['EntryTime'] and self.rif and self.tradesToday < p['MaxTradesPerDay']:
            r_rod = b.c / self.rif - 1
            if r_rod > 0:
                ctx.buy('LHH.L', p['NumContracts'])
            else:
                ctx.sell_short('LHH.S', p['NumContracts'])
            self.tradesToday += 1

        if mp != 0 and b.ora >= p['ExitTime']:
            ctx.sell('L.Flat')
            ctx.buy_to_cover('S.Flat')

        # il riferimento di oggi vale da domani: si aggiorna dopo aver usato quello di ieri
        if b.ora == p['ExitTime']:
            self.rif = b.c
