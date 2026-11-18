# Critica: regime_hmm_last_half_hour (destinazione prop)

**1. Tipo di fonte.** `paper` per l'effetto di base (Baltussen et al.); `idea propria` per il filtro HMM e per il legame regime-gamma. Applico il filtro paper alla madre e tratto il filtro come parametri senza prove.

**2. Filtro paper (domande 1-9)**

| # | esito | perché |
|---|---|---|
| 1 futures | sì (madre) | 17 futures su indici, S&P 500 incluso (p. 380). Il filtro HMM non è testato da nessuno |
| 2 replicato | sì (madre) | estende Gao et al., SPY 1993-2013. Il filtro non è replicato |
| 3 flusso obbligato | sì per la madre, no per il filtro | il gamma hedging è flusso; lo stato HMM non è gamma negativo: il paper non lega gamma a crisi o volatilità, e il gamma negativo è circa metà dei giorni (2.930 su 6.088) |
| 4 costi | no | il paper non li considera; accenna a un Sharpe positivo con 1 tick, senza numero |
| 5 intraday | sì | 1 trade/giorno max, 0,25-0,40 col filtro: da seconda gamba, meno di 1 |
| 6 età | no | 2021, oltre il picco di decadimento |
| 7 t ≥ 3 | sì sulla madre | t 4,72 (Tab. 8), 4,78 (gamma negativo), 1,03 (non negativo) |
| 8 oltre il 2021 | no | campione a maggio 2020; nostro test sulla madre: t −0,22 dopo maggio 2020; nessun follow-up aperto (Adams et al. non aperto) |
| 9 dati | sì | l'HMM usa solo prezzi del lake. Il gamma osservato no, ed è escluso dal prompt |

Pagine non verificate: il PDF scaricato è binario e non ho potuto leggerlo (nessun renderer, e il fetch non estrae il testo). Il salto di pagina fra p. 388 e p. 389 per le Tabelle 7 e 8 resta **non verificato**; i numeri sono quelli dell'ipotesi. Gao et al. e Ang-Timmermann non li ho riaperti: non cambiano il verdetto.

**3. Il conto (prop: 10 $/giorno per micro, netti, sui giorni di borsa)**

Edge dichiarato dal paper: 6,86% annuo / 252 = 2,7 bp per trade, lordo, su portafoglio 1/N di 17 indici, prima del 2020. Con NQ fra 15.000 e 20.000: 4-5 punti = 8-11 $ per micro (2 $/punto). Costo circa 2 $ per giro. Netto circa 6-9 $.

- **Prudente:** 0,25 trade/giorno × ~6 $ = **circa 1,5 $/giorno**. Nella realtà il t dopo il 2020 è −0,22: l'edge atteso è zero.
- **Favorevole:** frequenza massima della regola (la madre non filtrata, circa 1 trade/giorno) × 9 $ = **circa 9 $/giorno**, già sotto 10 senza nemmeno il filtro, che taglia il 60-75% dei trade. Col filtro (0,40/giorno) e un edge condizionato pari a 1,3 volte (β 6,63 contro 5,08, Tab. 7 e 8), 12 $ lordi, 10 netti: **4 $/giorno**. Anche raddoppiando i punti per la volatilità alta (speranza, non fonte): circa 7-8 $/giorno.
- Per arrivare a 10 $/giorno con 0,25-0,40 trade/giorno servono 25-40 $ netti per trade, 13-20 punti lordi: 3-5 volte l'edge del paper. Non plausibile per una mezz'ora senza stop.
- Potenza: con 300-500 trade, t ≥ 3 vuole media/dev. std ≥ 0,13-0,17 per trade; il paper, al meglio, ne dà circa 0,11. Anche con l'effetto pieno, t circa 2,2.

**4. Punti deboli**

1. **Il conto non passa nemmeno nel caso favorevole** (sopra): meno di mezzo trade al giorno contro 10 $/giorno.
2. **La madre è morta dopo maggio 2020** (t −0,22, 1.165 trade). Il filtro cerca un sottoinsieme in cui un effetto morto rivive: rischio di rumore selezionato. Nessuna fonte post-2021 sull'effetto condizionato.
3. **Il legame regime-gamma non ha fonte.** Il paper non collega gamma negativo e crisi; Ang-Timmermann (p. 14) mostra che «media bassa» e «volatilità alta» non coincidono sempre. Il nostro prompt dice che dal 2023 i dealer sono lunghi gamma quasi sempre.
4. **12 scelte libere**, tutte senza fonte (10 di Mario o dell'autore dell'ipotesi). L'HMM sarà quasi un filtro sulla volatilità a 20 giorni persistente. Il paper non fa questo condizionamento con un regime stimato.
5. **Misura non solida:** rendimenti percentuali su back-adjusted. Gao et al. è SPY e termina nel 2013.

Sui punti sollevati: (1) la serie precalcolata è deterministica, ma il prompt esclude i «modelli addestrati a runtime»; un input esterno non è codice PowerLanguage. Non basta da solo a uccidere, è un rischio di eseguibilità per il desk. (2) Il motore apre i dati prima del `dal` con il parametro `riscaldamento` (esegui.py, riga 46), e la serie P si calcola fuori dal motore dal CSV del lake dal 2016: il riscaldamento di 504 giorni non è un ostacolo. (3) Senza fonte: punto debole 3. (4) È il motivo del KILL.

**5.** RISERVA: sì (domanda 3 del filtro paper non soddisfatta per il filtro: il legame regime-gamma non è dimostrato; la domanda 8 è `no`).

**6.** KILL per il conto: nemmeno la madre non filtrata (circa 9 $/giorno con la frequenza massima e l'edge lordo del paper) arriva a 10 $/giorno per micro, e il filtro dimezza o peggio la frequenza.

VERDETTO: KILL
