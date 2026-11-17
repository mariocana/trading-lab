"""Gold Asian Range (strategies/GoldAsianRange/GoldAsianRange.txt), riga per riga.

Una serie: barre da 15 minuti su @GC. Con il template 24/7 di MC la barra di mezzanotte ha
Time = 2400, quindi `Time >= 2000` la include e la finestra va da 19:45 a 00:00 (17 barre); nel
CSV quella barra e' datata il giorno dopo con ora 0, qui la si rimappa a 2400 come fa MC.
"""

DEFAULT = dict(RangeStart=2000, RangeEnd=0, ExitTime=1000, StopFrac=1.0, TP_RR=0.0, TradeLongs=1,
               TradeShorts=1, MinRangePts=0.0, MaxRangePts=0.0, MaxRangePct=0.0, Num_Contracts=1)


class GAR:
    def __init__(self, **inp):
        self.p = dict(DEFAULT, **inp)
        self.inWindowPrev = False
        self.rHi, self.rLo, self.rng, self.sd = 0.0, 0.0, 0.0, 0.0
        self.armed = self.tradeDone = self.wasIn = False
        self.posSL = self.posTP = 0.0

    def su_barra(self, ctx):
        p, b = self.p, ctx.b()
        t = 2400 if b.ora == 0 else b.ora           # Time di MC con il template 24/7
        if p['RangeStart'] < p['RangeEnd']:
            inWindow = p['RangeStart'] <= t < p['RangeEnd']
        else:
            inWindow = t >= p['RangeStart'] or t < p['RangeEnd']

        if inWindow and not self.inWindowPrev:       # prima barra di una nuova finestra
            self.rHi, self.rLo, self.rng, self.sd = 0.0, 999999.0, 0.0, 0.0
            self.armed = self.tradeDone = False
        if inWindow:
            self.rHi = max(self.rHi, b.h)
            self.rLo = min(self.rLo, b.l)

        if not inWindow and self.inWindowPrev and self.rng == 0 and self.rHi > 0:
            self.rng = self.rHi - self.rLo
            self.sd = p['StopFrac'] * self.rng
            self.armed = (self.rng > 0
                          and (p['MinRangePts'] == 0 or self.rng >= p['MinRangePts'])
                          and (p['MaxRangePts'] == 0 or self.rng <= p['MaxRangePts'])
                          and (p['MaxRangePct'] == 0 or self.rng <= b.c * p['MaxRangePct'] / 100))
        self.inWindowPrev = inWindow

        mp = ctx.market_position
        if self.armed and not self.tradeDone and mp == 0 and t < p['ExitTime']:
            if p['TradeLongs'] == 1:
                ctx.buy('GAR-L', p['Num_Contracts'], self.rHi, 'stop')
            if p['TradeShorts'] == 1:
                ctx.sell_short('GAR-S', p['Num_Contracts'], self.rLo, 'stop')

        if mp != 0 and not self.wasIn:               # all'apertura: stop e target, disarma
            self.tradeDone, self.armed = True, False
            e = ctx.entry_price
            if mp == 1:
                self.posSL = e - self.sd
                self.posTP = e + p['TP_RR'] * self.sd if p['TP_RR'] > 0 else 0.0
            else:
                self.posSL = e + self.sd
                self.posTP = e - p['TP_RR'] * self.sd if p['TP_RR'] > 0 else 0.0
        self.wasIn = mp != 0

        if mp == 1:
            ctx.sell('L-SL', self.posSL, 'stop')
            if self.posTP > 0:
                ctx.sell('L-TP', self.posTP, 'limite')
        if mp == -1:
            ctx.buy_to_cover('S-SL', self.posSL, 'stop')
            if self.posTP > 0:
                ctx.buy_to_cover('S-TP', self.posTP, 'limite')

        if p['ExitTime'] <= t < p['RangeStart']:     # uscita a tempo
            if mp == 1:
                ctx.sell('EXIT-L')
            if mp == -1:
                ctx.buy_to_cover('EXIT-S')
            self.armed = False
