# Dossier — monday_long (16/11/2026)

- **L'idea**: long ES una volta a settimana, dalla domenica 19:00 CT al lunedì 15:55 CT, stop 90 punti, target 100, lunedì festivi esclusi.
- **Il critico**: GO con `RISERVA: sì`. Fonte da praticante non verificabile (P2, P3, P6), la scheda dell'autore dice che l'effetto decade. Mario ha deciso di spendere la misura.
- **La misura**: SOTTO SOGLIA. 2,75 errori standard contro 3,0 e $4,98 al giorno per micro contro $10.

## La misura (in-sample 2020-01-01 → 2024-12-31, ES 1 minuto, $15 per lato)

| | |
|---|---|
| trade | 231 (0,18 al giorno su 1.299 giorni) |
| WR | 59,31% |
| R:R realizzato | 0,990 |
| il caso (null) | 50,26% |
| eccesso | +9,05 pp |
| errore standard | 3,29 pp |
| errori standard | 2,75 (minimo 3,0) |
| t della media | 2,10 |
| media per trade | $279,79 per ES, $27,98 per micro |
| $ al giorno per micro | 4,98 (minimo 10,0) |

Il file è `misura.json`. La soglia scritta dal ricercatore nell'ipotesi era quella del perimetro, non più severa.

## Tre note del desk

1. **Il muro è stato rotto con il ricercatore.** Il desk gli ha passato per errore la SPEC intera, che riportava una misura del 10/11 sulla stessa finestra senza stop e con i festivi (257 lunedì, t 2,51). Il ricercatore lo dichiara nella sezione 7 dell'ipotesi; la soglia è quella del perimetro e non dipende da quei numeri. La fonte è stata ripulita prima del critico e del coder.
2. **Manca il lunedì 16/03/2020.** Domenica 15/03/2020 il minuto delle 19:00 non esiste nei dati (limit down) e la regola dell'ipotesi dice che quel lunedì non si trada: 231 trade invece di 232. In MultiCharts, su barre da 5 minuti, quel trade può esserci.
3. **Ingresso e uscita un minuto dopo.** Il motore non ha l'ordine alla chiusura della barra: si entra all'apertura delle 19:01 e si esce all'apertura delle 15:56.

## I documenti

- Ipotesi: `hypothesis.md`
- Critica: `critique.md`
- Fonte: `fonti/idea.md`
- Regola: `multicharts/motore/strategie/monday_long.py`
