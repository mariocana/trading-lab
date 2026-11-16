# monday_long, critica

**1. Tipo di fonte:** `praticante` (Triple Open, The Bridge). La forma registrata, senza EMA e con
lo stop, non l'ha misurata nessuno.

**2. Filtro P1-P6**

| voce | esito | perché |
|---|---|---|
| P1 codice o regole complete | sì | la regola in `hypothesis.md` è completa e non ha parametri liberi; il codice dell'autore non è verificato |
| P2 dati oltre il 2021 | non verificato | lo sappiamo solo dalla trascrizione; `protocollo/` non si apre |
| P3 OOS dichiarato e separato | non verificato | solo dalla trascrizione, e riguarda un'altra forma (EMA, niente stop); 2024 «quasi piatto» |
| P4 flat entro la sessione | sì | una sola sessione Globex, esce alle 15:55 CT |
| P5 stop dichiarato prima | no | l'autore non ha stop; il 90 lo fissa Mario prima della misura, dal tetto di rischio |
| P6 costi o edge lordo ≥ 3× costo | non verificato | non sappiamo se la scheda dichiara i costi; nessun edge per trade alla pagina |
| testata sui nostri futures | non verificato | ES secondo la trascrizione |
| track record live | non verificato | non dichiarato |
| trade nell'OOS | non verificato | non dichiarato; a uno a settimana su circa 2,7 anni sarebbero circa 130 |
| parametri ottimizzati | non verificato | la finestra viene da una ricerca sugli orari, con un numero di prove ignoto |
| chi perde | non lo so | lo scrive anche l'ipotesi |

**3. Il conto** (ES $50/pt, micro $5/pt, costo $3 a giro per micro)

- **Frequenza.** La regola permette al massimo 232 trade su circa 1.300 giorni, cioè circa 0,18
  al giorno. Il caso prudente e quello favorevole hanno la stessa frequenza.
- **Costi:** $3 × 0,18, circa $0,54 al giorno per micro. Non sono il problema.
- **Cosa serve.** Per $10 al giorno: $13.000 / 232, circa $56 netti per trade, cioè 11,2 punti
  netti e circa **11,8 lordi** per lunedì.
- **Nessuna fonte dichiara un edge.** L'unico riferimento è il «profilo atteso» della SPEC, WR
  55-62% con R:R intorno a 1. È l'attesa di Mario, non un dato.
- **Prudente (WR 55%, R:R 1).** Il guadagno atteso è 0,10 × la vincita media, quindi la vincita
  media dovrebbe essere circa 118 punti. Il target è 100: **non passa, per geometria.**
- **Favorevole (WR 62%, R:R 1).** Il guadagno atteso è 0,24 × la vincita media, quindi servono
  vincite e perdite medie di circa 49 punti. La geometria (90/100) lo permette, ma nessuna fonte
  lo dichiara. Il conto resta **indeterminato, non bocciato.**
- **Plausibilità.** 11,8 punti lordi × 232 lunedì fanno circa 2.700 punti, all'incirca tutto il
  rialzo di ES dal 2020 al 2024. È plausibile solo nel caso migliore.

**4. Punti deboli**

1. **Le fonti non sono verificate, e la regola non è dell'autore.** Nessun numero è stato
   verificato alla pagina. P2, P3 e P6 non sono verificati. L'autore scrive che l'effetto decade
   e che nessuna delle tre strategie passa da sola.
2. **Il conto passa solo nel caso favorevole.** Nel caso prudente non passa per geometria. Nel
   caso favorevole i soli lunedì devono rendere quanto l'intero rialzo dell'indice.
3. **L'eccesso sul random walk non isola il lunedì.** Un long di 21 ore in un mercato che sale
   vince più spesso del caso per il solo drift. Non c'è un flusso obbligato e il perdente non è
   identificato.
4. **Le fonti sono contro, o morte.** Metà del trade è overnight drift, morto dopo il 2021. Il
   campione dell'effetto weekend inverso finisce nel 1998. Kamstra-Kramer-Levi va nella
   direzione opposta: lunedì negativi dopo il cambio dell'ora.
5. **L'in-sample non è cieco.** La finestra è stata scelta con una ricerca sugli orari, e il
   nostro 2020-2023 è quasi certamente il periodo su cui è stata scelta. Il desk ha già guardato
   la stessa regola senza stop sul nostro IS, più tre varianti su dati proxy. La prima riga di
   `fonti/idea.md` («mai stata girata») contraddice l'ipotesi su questo punto.

Varianti non dichiarate: nessuna. La parentela con l'overnight drift è dichiarata, e nessuna
sorella in `ricerca/idee/` ha la stessa regola.

RISERVA: sì. Mancano tre voci eliminatorie per un praticante: P2, P3 e P6 non sono verificate.
Inoltre la fonte più vicina dice che l'effetto decade e che da sola la strategia non passa.

VERDETTO: GO
