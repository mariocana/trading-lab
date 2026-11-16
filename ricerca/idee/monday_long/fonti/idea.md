> Idea di Mario: la SPEC pre-registrata il 10/11/2026 in multicharts/strategies/MondayLong/SPEC.md, scritta prima di qualsiasi run. La strategia non e mai stata girata. La regola da misurare e questa, senza varianti.

# SPEC — MondayLong, ES → MES (Stage 0, 10/11/2026)

**Ipotesi**: il lunedì l'S&P 500 sale più spesso di quanto scenda. Si compra alla chiusura della
barra delle 19:00 CT della domenica, la prima ora piena della sessione Globex che appartiene al
lunedì, e si esce alle 15:55 CT del lunedì. Nessun filtro: è la famiglia "long del lunedì" nella
sua forma nuda, con l'unica aggiunta di uno stop sul prezzo.

**Perché**: due letture, nessuna delle due forte.
- *Effetto weekend inverso* (Brusa, Liu, Schulman 2005): dalla fine degli anni '80 sulle large
  cap il rendimento del lunedì non è più negativo ma positivo, soprattutto dopo un venerdì in
  rialzo. È la lettura più vicina a questo trade: ES è un indice di large cap.
- *Cambio dell'ora legale* (Kamstra, Kramer, Levi 2000): il paper chiedeva uno **short** nel
  lunedì dopo il cambio d'ora, due settimane l'anno. L'autore del codice scrive che "la zona
  selezionata è diventata Monday long": la finestra 19:00 → 15:55 è uscita da una ricerca su
  orari, non dal paper. Il paper non sostiene questo trade, lo ha solo ispirato.

Il meccanismo plausibile è un flusso: chi alleggerisce il venerdì per non portare rischio nel
weekend ricompra il lunedì, e lo fa dopo aver visto che il weekend non ha portato notizie.

**Chi perde**: chi vende nella Globex sottile della domenica sera e chi si è coperto per il
weekend e ricopre il lunedì a prezzi più alti. Lo diciamo come ipotesi: non abbiamo un modo di
misurarlo.

**Fonte**: "Triple Open", The Bridge del corso,
`protocollo/9.TheBridge/STRATEGIES/PROP FIRM COMPLEMENTARY/`: `1. Monday Long ES (EMA distance
filter).txt` (L644ES, v2.1), `1. Monday after an up Friday ES.txt` (L656ES), `1. Monday Long NQ
(ADX filter).txt` (L644NQ) e la scheda `1. Triple_Open.pdf`. I file originali restano lì e non si
toccano. La nostra versione è lo scheletro di L644ES **senza il filtro EMA** e **con uno stop**.

## Cosa la distingue da quello che è già stato provato

- **Overnight drift** (chiuso, gli autori lo danno per morto dopo il 2021) è il parente più
  vicino: questo trade tiene la domenica sera e la notte del lunedì, e quel pezzo **è** overnight
  drift. La differenza: qui si tiene una volta a settimana, dentro una sola sessione, e si porta
  anche tutta la RTH del lunedì. È un effetto di giorno della settimana, non di ora del giorno. Se
  l'overnight drift è morto, una parte di questo è morta con lui: il profilo per anno lo dirà
  (vedi Rischi), ma non lo si usa per cambiare le regole.
- **Last Half-Hour**: effetto di calendario intraday morto dopo la pubblicazione. Stesso rischio
  qui: weekend e ora legale sono effetti pubblicati da più di vent'anni e la scheda dell'autore
  lo scrive da sola ("calendar anomalies decay", 2024 quasi piatto).
- **Ciclo settimanale lunedì-mercoledì** di un altro corso: trascritto, mai testato. Nessun
  numero da cui partire.
- **DriftPullback e Overnight Bias ORB**, nel book, tradano NQ anche il lunedì in RTH. Questo è
  long ES nelle stesse ore del lunedì: la correlazione col book è il punto del gate (fase 3b),
  non un dettaglio.

## Regole

| | |
|---|---|
| Famiglia | calendario · giorno della settimana · solo long |
| Strumento · TF · sessione | @ES (sviluppo) → **MES** · **5 min** · CME Globex **17:00-16:00 CT senza pause**, timezone **Exchange (CT)**, barre timbrate alla chiusura · Bar Magnifier **1 min** |
| Armamento | nessun filtro. La sessione è quella del lunedì (una barra dopo le 16:30 CT appartiene alla sessione del giorno dopo, come nel codice dell'autore) e il lunedì **non** è un festivo NYSE né una chiusura anticipata |
| Trigger | **Buy this bar on close** sulla barra delle **19:00 CT** della domenica (la barra 18:55-19:00). Una volta a settimana, solo se flat |
| Exit | **stop 90 punti** sul prezzo d'ingresso, attivo dalla prima barra dopo l'ingresso (l'ingresso è sulla chiusura della barra delle 19:00, quindi non c'è barra scoperta) · **target +100 punti**, backstop come nell'originale · **uscita a tempo** alla chiusura della barra delle **15:55 CT** del lunedì (`Sell this bar on close`), con la barra delle 16:00 come rete se la 15:55 manca |
| Guardrail | max 1 trade a settimana, mai due posizioni. Nessun trade se il lunedì è festivo o a chiusura anticipata |
| Trade/giorno | 0-1 (un trade per sessione del lunedì; nella List of Trades l'ingresso porta la data della **domenica**) |
| Profilo atteso | WR 55-62%, R:R (vincita media / perdita media) intorno a 1, perdita massima per trade fissata dallo stop |

**Festivi.** Esclusi i lunedì in cui la NYSE è chiusa (Capodanno osservato, Martin Luther King,
Presidents' Day, Memorial Day, Juneteenth dal 2022, 4 luglio osservato, Labor Day, Natale
osservato) o chiude alle 13:00 ET (3 luglio se lun-gio; 24 dicembre se lun-gio). Il calendario si
calcola per regola come nel blocco "HOLIDAY CALENDAR" di L644ES v2.1, che si può riprendere così
com'è (incluso il calcolo della Pasqua, che non tocca i lunedì ma non dà fastidio). Le chiusure
straordinarie (lutto nazionale) non sono gestite, come nell'originale: nel 2020-2026 nessuna è
caduta di lunedì.

**Conteggio atteso dei trade** (calcolato dal calendario, non dai dati):
**IS 2020-2024: 232 lunedì** tradabili su 261 (29 esclusi). OOS 01/01/2025 → 09/11/2026:
89. Uno o due in meno sono possibili se mancano barre nei dati; di più è un bug.

**Lo stop è l'unica modifica rispetto all'originale**, che non ha stop (`StopPts 0`). Non viene
dai dati: viene dalla regola della via B, trade peggiore ≤ $500 per micro (conti sotto).

**IS**: 2020-01-01 → 2024-12-31 · **OOS**: 2025-01-01 → oggi.
Non serve lead-in: niente indicatori. Il calendario dei festivi si costruisce sulla prima barra di
ogni anno, per l'anno e il successivo.

## Conti (1 contratto; ES = $50/pt, MES = $5/pt)

Costi: **$15 per lato** nel campo commissione di @ES, slippage incluso, slippage di MC a 0 →
**$30 a giro per ES, $3 per MES**.

| | punti ES | @ES | MES |
|---|---|---|---|
| Stop | 90 | $4.500 + $30 = **$4.530** | **$453** |
| Target | 100 | $5.000 − $30 = **$4.970** | **$497** |
| Margine sotto il tetto di via B ($500 per micro) | 9,4 | $470 | **$47** |
| **Worst day** (un trade, uno stop) | | **$4.530** | **$453** |

**Perché 90 e non 99.** $500 per micro = $5.000 per ES = 100 punti lordi. Tolti $30 di costi il
massimo teorico è 99,4 punti. Con 90 restano 9,4 punti di ES (circa 37 tick) di margine per lo
slippage dello stop: nel backtest con Bar Magnifier lo stop si riempie al suo prezzo salvo che la
barra a 1 minuto apra già oltre; dal vivo la domenica sera il book è sottile. 95 punti
lascerebbero 4,4 punti, troppo poco per un ordine stop in Globex notturna. 90 è fissato qui e non
si tocca.

**Il trade non attraversa la pausa delle 16:00-17:00 CT**: entra dopo la riapertura della
domenica (il gap del weekend è già nel prezzo d'ingresso, lo stop non lo vede mai) ed esce alle
15:55 del lunedì. Per una prop che conta il giorno per sessione 17:00-16:00 CT è **un solo giorno
di trading**, il lunedì: il worst day è il singolo stop, $453 per micro, contro una DLL di Lucid
di $1.200.

**Stage 1 e "flat la sera".** Il trade attraversa la mezzanotte: nella List of Trades ingresso
la domenica, uscita il lunedì. Il controllo `--flat` di `lab.py` (nessun trade a cavallo di due
date) qui **non si applica** e non va passato: il flat che conta è "nessuna posizione dopo le
16:00 CT del lunedì", da controllare sugli orari d'uscita.


> Il resto della SPEC (contaminazione, rischi, criteri per fase, varianti, setup) e stato tolto dal desk il 16/11: contiene numeri di una misura precedente, che ricercatore, critico e coder non devono vedere. Il testo intero e in multicharts/strategies/MondayLong/SPEC.md e non va aperto. Fatti che servono senza numeri: la finestra oraria e stata scelta dall autore con una ricerca su orari; l autore ha pubblicato un fuori campione 2024-01-07 -> 2026-09-21; la regola qui e la sua senza il filtro EMA e con lo stop aggiunto.
