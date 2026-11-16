> Idea di Mario, come l'aveva scritta prima di qualsiasi misura. Fonte: strategia di un praticante (corso).

# SPEC — Overnight Bias ORB, NQ (Stage 0, 29/10/2026)

**Fonte:** `education/protocollo/9.TheBridge/STRATEGIES/PROP FIRM NATIVE HIGH RR/Overnight Bias ORB.txt`
(OFB_OvernightBiasORB_Signal), unico file della cartella «high RR» del corso.
**Codice:** `OvernightBiasORB.txt`, in MultiCharts `Mario_OvernightBiasORB`. La logica è quella
dell'autore riga per riga. Cambiano solo gli orari di default, in CT invece che in ET, e la
finestra `TradeStartEL` / `TradeEndEL`, che separa il lead-in dal periodo valutato.

## Ipotesi

Dove apre il cash rispetto al range della notte dice chi ha il controllo. Un open nel terzo
alto del range overnight rende probabile la continuazione al rialzo, uno nel terzo basso al
ribasso. Si compra solo il breakout dell'opening range a 15 minuti in quella direzione. Il
movimento deve avere trend (ADX ≥ 20), non deve partire da una barra di esaurimento e la
giornata deve avere un range «normale». Target 3 volte lo stop: pochi trade vinti, ma grandi.

**Perché dovrebbe funzionare:** l'overnight è il posizionamento di chi ha già agito; l'apertura
nella stessa direzione lo conferma. Chi perde: chi fada il breakout d'apertura nei giorni di
trend.

| | |
|---|---|
| Famiglia | breakout del range di apertura · momentum, con filtro di bias |
| Strumento · TF · sessione | @NQ → MNQ · **15 min** · **Globex**, timezone Exchange (CT) |
| Overnight | dalla **mezzanotte CT** (cambio data) alle 08:30. Non dalle 17:00: è la scelta dell'autore |
| Bias | open ≥ 67% del range overnight → solo long; ≤ 33% → solo short; in mezzo niente |
| Opening range | 08:30–08:45 CT. Giorno scartato se il range supera 2 volte la sua media (EMA 20) |
| Entry | prima chiusura oltre l'OR nel verso del bias, 08:45–12:00 CT, ADX(16) ≥ 20, barra ≤ 2,5 volte la media di 20 → next bar at market |
| Stop | 0,30 × ATR giornaliero RTH (15 giorni), dalla close del segnale |
| Target | 3 × stop |
| Altre uscite | flat 14:30 CT |
| Trade/giorno | max 4, una posizione alla volta |

## I numeri dell'autore (header del codice, costi zero, 1 NQ)

| | trade | PF | net | DD |
|---|---|---|---|---|
| IS 2006–2019 | 1.112 | 1,35 | $50.445 | $6.160 |
| OOS 2020 → 08/2026 | 599 | **1,66** | $257.615 | **$20.195** |

- **Avg OOS ~$430 per NQ lordo**, ~$415 dopo $15 di costi: ~$41 per micro.
- **DD OOS $20.195 per NQ = ~$2.020 per micro, l'intero MLL di Lucid.** Fuori dal profilo
  WR 54–72% e R:R 0,5–1 per costruzione: con R:R 3 il WR atteso è intorno al 35%.

## Live 006: il corso la usa con R:R 1,5 (29/10/2026)

Nel book «Balanced» della Live 006 Overnight Bias gira a **1 MNQ con `TakeProfitRR 1.5`**. L'1,5
è scelto fra 5 uscite su gen 2023 → ago 2025, e la nota della slide 14 dice che con il 3 originale
il book faceva lo stesso (EV $5.803 contro $5.590). **Qui resta 3**, il default del codice: cambiarlo
sarebbe una variante scelta a posteriori. Analisi in `mc/docs/live006_funded.md`.

