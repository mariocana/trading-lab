# Critica: prova2_overnight_bias

**Tipo di fonte:** `praticante`. È il codice di un corso, «The Bridge», `Overnight Bias ORB.txt`.
In `fonti/` c'è solo la trascrizione di Mario (`idea.md`), non il file originale.

## Filtro P1-P6

| voce | esito | perché |
|---|---|---|
| P1 codice o regole complete | sì | Il codice PowerLanguage è completo e tutti i parametri sono fissati. Le [scelta] della scheda cedono al codice dell'autore |
| P2 dati oltre il 2021 | sì | L'header del codice dichiara un OOS fino ad agosto 2026. Lo sappiamo dalla trascrizione, il file originale non è in `fonti/` |
| P3 OOS dichiarato e separato | non verificato | Sulla carta è separato (2006-2019 e 2020-2026), ma la data del codice non si conosce. Il PF dell'OOS (1,66) è più alto di quello dell'IS (1,35), il segno tipico di una regola tarata sul periodo recente |
| P4 flat entro la sessione | sì | Esce a mercato alle 14:30 CT |
| P5 stop dichiarato | no | Lo stop è 0,30 × ATR(15) RTH senza tetto. P5 chiede «ATR con tetto». L'uscita c'è, quindi non elimina |
| P6 costi o lordo ≥ 3× costo | sì | I costi dichiarati sono zero, ma il lordo dichiarato (~$430/NQ) vale circa 29 volte i $15 andata e ritorno |
| testata sui nostri futures | sì | NQ |
| track record live | non verificato | Il corso la usa nella Live 006, ma con 1,5R e senza risultati live di questa regola |
| trade nell'OOS | sì | 599, sopra i 100 |
| parametri ottimizzati | non verificato | Non dichiarati. I valori fissati sono una decina (67/33, EMA 20 e 2×, ADX 16/20, 2,5× su 20, 0,30 × ATR 15, 3R, finestre orarie) |
| chi perde | debole | «Chi fada il breakout nei giorni di trend»: nessun soggetto preciso |

## Il conto (per micro, costo $1,5 andata e ritorno)

- **Caso prudente.** Prendo l'edge dell'IS 2006-2019: $50.445 / 1.112 = $45 a trade per NQ, cioè $4,5 per micro, che dopo i costi diventano $3,0. La frequenza dichiarata è 0,32 trade al giorno. 0,32 × $3,0 = **~$1 al giorno**, contro un minimo di $10. **Non passa.**
- **Caso favorevole, con la frequenza dichiarata.** Prendo l'edge dell'OOS: $257.615 / 599 = $430 per NQ, cioè $43 per micro, che dopo i costi diventano $41,5. La frequenza è 0,36 al giorno. 0,36 × $41,5 = **~$15 al giorno**. Passa, con poco margine.
- **Caso favorevole, con la frequenza massima che la regola permette.** 4 trade al giorno × $41,5 = $166 al giorno. Passa, ma è un numero teorico: l'autore stesso ne registra 0,36.

Nel caso favorevole il conto passa, quindi non è un KILL.

## Punti deboli

1. **L'OOS potrebbe non essere un OOS (P3 non verificato).** La data del codice non si conosce, il PF dell'OOS supera quello dell'IS, e il nostro 2020-2024 sta tutto dentro il periodo che l'autore può aver usato per scegliere le regole. In più i numeri arrivano da una trascrizione: il file originale non è in `fonti/`.
2. **La frequenza.** L'autore dichiara 0,32-0,36 trade al giorno, circa un terzo del minimo di 1. Il tetto teorico di 4 la tiene dentro il perimetro, ma con ogni probabilità la misura la boccia su questo da sola.
3. **Nessun flusso obbligato e un perdente vago.** È un ORB di momentum con un filtro di bias, cioè un pattern comportamentale. Il prior è basso.
4. **Lo stop scala con l'ATR senza tetto (P5 «no» sulla lettera).** Il drawdown OOS dichiarato è di $20.195 per NQ. Con un target a 3R e il 35% circa di vincite, il risultato può dipendere da poche giornate.
5. **Una decina di parametri fissati, quanti ottimizzati non si sa.** Inoltre il 2020-2024 è un periodo di forte rialzo di NQ: il risultato va diviso fra long e short.

RISERVA: sì. P3, che per un praticante è eliminatoria, è `non verificato`.

VERDETTO: GO
