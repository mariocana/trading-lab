# monday_long

**Parentela, da leggere prima.** Non è la variante di un'idea morta, ma una sua parte lo è: la
gamba domenica sera e notte del lunedì (19:00 → 08:30 CT) è **overnight drift** (Boyarchenko,
Larsen, Whelan), chiuso nel cimitero e dato per morto dagli autori dopo il 2021. Il resto del
trade è la RTH del lunedì. È la prima idea «giorno della settimana» del registro.

## Ipotesi

Un long su ES tenuto dalle 19:00 CT di domenica alle 15:55 CT di lunedì, con stop a 90 punti e
target a 100, vince più spesso di un random walk con la stessa geometria. Il margine deve bastare
a coprire i costi con un solo trade a settimana. È falsa se l'eccesso sul caso nell'in-sample
2020-2024 sta sotto 3 errori standard, o se il guadagno netto sta sotto $10 al giorno per micro.

## Meccanismo

Mario lo propone come flusso: chi alleggerisce il venerdì per non portare rischio nel weekend
ricompra il lunedì, dopo aver visto che il weekend non ha portato notizie. È un'ipotesi. Non è un
flusso obbligato nel senso del filtro dei paper: nessun mandato, benchmark o hedge costringe a
ricomprare proprio il lunedì.

La seconda lettura di Mario è l'effetto weekend «inverso» sulle large cap (Brusa, Liu, Schulman):
un pattern documentato su dati degli anni '90, senza un meccanismo forzato.

C'è una terza lettura, più semplice, da tenere presente. Un long su ES tenuto circa 21 ore, in un
periodo in cui l'indice sale, guadagna anche senza nessun effetto del lunedì: si porta dentro la
notte (overnight drift) e il drift di fondo dell'indice.

## Chi perde, e perché continua a perdere

Mario nomina due candidati:
- chi vende nella Globex sottile della domenica sera;
- chi si è coperto per il weekend e ricopre il lunedì a prezzi più alti.

La SPEC stessa dice che è un'ipotesi e che non abbiamo un modo di misurarla. Io non so spiegare
perché questi operatori continuerebbero a pagare dopo vent'anni di pubblicazioni sull'effetto
weekend. L'argomento più forte che ho è debole: chi si copre per il weekend paga
un'assicurazione, e può accettarne il costo.

**Chi perde: non stabilito.**

## Fonti

**Tipo: `praticante`.** Va letto con il filtro P1-P6.

Va detto subito: la regola registrata **non è quella dell'autore**. Mario ha tolto il filtro EMA
e ha aggiunto lo stop, e nessuna fonte ha misurato questa forma. Per la regola esatta il tipo vero
è vicino a `idea propria`.

**1. Il praticante: «Triple Open», The Bridge del corso.**

- **Dove:** `protocollo/9.TheBridge/STRATEGIES/PROP FIRM COMPLEMENTARY/`. I file sono:
  - `1. Monday Long ES (EMA distance filter).txt` (L644ES v2.1);
  - `1. Monday after an up Friday ES.txt` (L656ES);
  - `1. Monday Long NQ (ADX filter).txt` (L644NQ);
  - la scheda `1. Triple_Open.pdf`.
- **Non verificato.** Questi file non sono nel repository: `protocollo/` non è stato importato, e
  una ricerca di «Triple» non trova niente. Tutto quello che segue lo so solo dalla trascrizione
  di Mario in `fonti/idea.md`.
- **Di verificato** c'è solo il nostro codice, `multicharts/strategies/MondayLong/MondayLong.txt`.
  Dice di ricalcare scheletro e calendario dei festivi di L644ES.
- **Cosa dichiara l'autore**, secondo la trascrizione:
  - la finestra 19:00 → 15:55 è «la zona selezionata» di una ricerca sugli orari: l'autore ha
    provato un numero di finestre che non conosciamo;
  - l'originale non ha stop (`StopPts 0`);
  - la scheda ha un out-of-sample 2024-01-07 → 2026-09-21, con il profitto concentrato nel
    2025-2026 e il 2024 «quasi piatto»;
  - la scheda dice «calendar anomalies decay»;
  - l'autore scrive che nessuna delle tre strategie passa da sola una soglia OOS severa. Le
    propone come aggiunta a un book, contro la chiusura per inattività di un conto funded.
- **Nessun numero di edge per trade** che io possa mettere su una pagina.
- **P1-P6**, per quanto lo so:
  - **P1 sì secondo la trascrizione**, non verificato: il codice dell'autore esiste;
  - **P2 sì secondo la trascrizione**, non verificato: la scheda arriva al 2026;
  - **P3 dichiarato secondo la trascrizione**, non verificato. L'OOS dell'autore parte il
    07/01/2024, quindi il nostro 2024 ci sta dentro. Il nostro 2020-2023 è con ogni probabilità
    il periodo su cui l'autore ha scelto la finestra;
  - **P4 sì**: entra ed esce nella stessa sessione Globex;
  - **P5 no per l'autore**, che non ha stop. Lo stop a 90 lo mette Mario, per la regola della
    via B (trade peggiore ≤ $500 per micro), non per i dati;
  - **P6 non verificato**: non so se la scheda dichiara i costi.

**2. Brusa, J., Liu, P., Schulman, C. (2005).** «Weekend Effect, "Reverse" Weekend Effect, and
Investor Trading Activities», *Journal of Business Finance & Accounting* 32(7-8), 1495-1517.
[RePEc](https://econpapers.repec.org/RePEc:bla:jbfnac:v:32:y:2005:i:7-8:p:1495-1517).

- Ho visto solo la scheda bibliografica e l'abstract, non il testo.
- Secondo l'abstract, sul 1988-1998 il rendimento del lunedì delle large cap è positivo: è
  l'effetto weekend inverso. Il classico effetto weekend negativo sta sulle small cap.
- **Nessun numero di questo paper entra**: non ho la pagina.
- Il campione finisce nel 1998. Con la domanda 8, eliminatoria per i paper, non entrerebbe come
  fonte dell'effetto: qui fa solo da contesto.

**3. Kamstra, M., Kramer, L., Levi, M. (2000).** «Losing Sleep at the Market: The Daylight Saving
Anomaly», *American Economic Review* 90(4), 1005-1011.
[RePEc](https://ideas.repec.org/a/aea/aecrev/v90y2000i4p1005-1011.html).

- Ho visto solo la scheda bibliografica.
- Dice il **contrario** di questo trade: rendimenti negativi il lunedì dopo il cambio dell'ora,
  due lunedì l'anno.
- Secondo la trascrizione, l'autore del corso ne ha preso lo spunto ed è arrivato a un long con
  una ricerca sugli orari. Il paper non sostiene questo trade.
- **Nessun numero entra.**

**Fonti con un numero verificato alla pagina: zero.**

## Regola eseguibile

È quella della SPEC di Mario e di `MondayLong.txt`, senza varianti.

**Perimetro.** L'ingresso è domenica alle 19:00 CT, l'uscita lunedì alle 15:55 CT. Le date sono
due, ma la sessione è una sola, quella Globex del lunedì (17:00 di domenica → 16:00 di lunedì). Il
trade chiude prima della fine della sessione, quindi è intraday nel senso del perimetro.

**Dati e mercato**
- ES continuous back-adjusted, barre a 1 minuto del lake, ora di Chicago (Exchange), barre timbrate
  alla chiusura, sessione Globex 17:00-16:00 CT senza pause.
- La SPEC usa barre da 5 minuti con Bar Magnifier a 1 minuto. Nel motore si usano le barre a 1
  minuto: la barra 18:55-19:00 a 5 minuti e il minuto timbrato 19:00 chiudono allo stesso prezzo.
- Gli orari sono in CT e non si convertono, nemmeno nelle settimane del cambio d'ora.
- Una barra con ora > 16:30 appartiene alla sessione del giorno dopo: la domenica sera è già
  lunedì.

**Setup.** La sessione è quella di un lunedì, e quel lunedì non è né festivo NYSE né a chiusura
anticipata (calendario sotto). Nessun altro filtro.

**Ingresso**
- Long a mercato, 1 contratto, alla chiusura del minuto timbrato **19:00 CT** di domenica. Solo se
  flat.
- Il motore non esegue «alla chiusura di questa barra». Un ordine a mercato dato alla chiusura del
  minuto delle 19:00 si riempie **all'apertura del minuto 19:01**: la differenza è al più un tick o
  due. Va scritto nel dossier, non va corretto.
- Se il minuto delle 19:00 manca nei dati, quel lunedì non si trada: niente ingresso al minuto
  dopo.

**Stop**
- 90 punti sotto il prezzo d'ingresso, ordine stop.
- Nel motore le uscite partono dalla chiusura della barra d'ingresso, come in MultiCharts. Con le
  barre a 1 minuto il minuto 19:01 resta quindi senza stop, e lo stop è attivo dal minuto 19:02.
- Se un minuto apre già sotto lo stop (gap, come il limit down del 15/03/2020), il fill è
  all'apertura di quel minuto, come fa il motore. Quel trade conta per intero: niente tetto alla
  perdita.

**Target**
- 100 punti sopra il prezzo d'ingresso, ordine limite, attivo dagli stessi minuti dello stop.
- «Backstop come nell'originale», nella SPEC, vuol dire solo questo: nel codice è un
  `SetProfitTarget` di 100 punti e nient'altro.
- Se stop e target cadono nello stesso minuto, decide il motore con il percorso del minuto (open →
  estremo più vicino → l'altro → close), come il Bar Magnifier di MultiCharts.

**Uscita a tempo**
- A mercato alla chiusura del minuto timbrato **15:55 CT** del lunedì. Nel motore si riempie
  all'apertura del minuto 15:56.
- Se il minuto delle 15:55 manca, esce al primo minuto successivo. La rete finale è la chiusura
  della sessione alle 16:00.

**Mezzanotte.** Il trade cambia data ma non cambia sessione. Il flat a fine sessione
(`esci_a_chiusura`) e la pausa di sessione del motore devono chiuderlo solo alle 16:00 del lunedì,
**non a mezzanotte né al cambio di data**.

**Massimo.** Un trade per sessione del lunedì: al massimo uno a settimana, mai due posizioni.

**Calendario dei festivi**, calcolato per regola e non da un file.
- Lunedì esclusi perché la NYSE è chiusa:
  - Capodanno osservato: 1/1, o lunedì 2/1 se l'1/1 cade di domenica; se cade di sabato non si
    osserva;
  - Martin Luther King: terzo lunedì di gennaio;
  - Presidents' Day: terzo lunedì di febbraio;
  - Memorial Day: ultimo lunedì di maggio;
  - Juneteenth, dal 2022: 19/6, o lunedì 20/6 se il 19 cade di domenica;
  - 4 luglio: 4/7, o lunedì 5/7 se il 4 cade di domenica;
  - Labor Day: primo lunedì di settembre;
  - Natale: 25/12, o lunedì 26/12 se il 25 cade di domenica.
- Lunedì esclusi perché la NYSE chiude alle 13:00 ET: il 3/7 e il 24/12, quando cadono di lunedì.
- Chiusure straordinarie: non gestite. Nel 2020-2024 nessuna è caduta di lunedì.

**Controllo per il coder, dal solo calendario.** Sul 2020-2024 i lunedì sono 261. Gli esclusi sono
29:
- i 20 lunedì fissi, cioè MLK, Presidents', Memorial e Labor Day per cinque anni;
- più nove: 05/07/2021, 20/06/2022, 04/07/2022, 26/12/2022, 02/01/2023, 19/06/2023,
  03/07/2023 (chiusura anticipata), 25/12/2023, 01/01/2024.

I lunedì tradabili sono **232**. Uno o due trade in meno vanno bene, se mancano barre. Più di 232,
o più di due in meno, è un errore della regola.

**Costi.** $15 per lato per ES, slippage incluso: $30 a giro, $3 per micro. Valore del punto $50.

**Parametri.** Nessuno libero. 19:00, 15:55, 90 e 100 li ha fissati Mario prima della misura:
- orari e target vengono dall'autore;
- lo stop viene dal tetto di rischio della via B, non dai dati.

## Frequenza e costi

**Segnali al giorno: circa 0,18.** Sono 232 trade su circa 1.300 giorni feriali con barre (il
denominatore di `misura.py`): 46 l'anno, uno a settimana meno i festivi.

**Cosa serve per il minimo in dollari**
- $10 al giorno per micro su circa 1.300 giorni sono circa $13.000 per micro in cinque anni.
- Divisi per 232 trade fanno **circa $56 netti per trade per micro**.
- In punti ES: circa **11,1 netti per lunedì**, circa **11,7 lordi** con il costo di 0,6 punti a
  giro.

**Il costo per trade non è il problema.** 0,6 punti sono pochi contro un movimento di 21 ore: il
conto dei costi da solo non uccide l'idea.

**Il problema è il conto in dollari.**
- 11,7 punti × 232 lunedì fanno circa 2.700 punti.
- È all'incirca tutto il rialzo di ES dall'inizio del 2020 alla fine del 2024: conoscenza
  generale, ordine di grandezza, non una misura.
- Per passare il minimo, i soli lunedì dovrebbero rendere quanto l'intero periodo.

**Il confronto con la fonte non si può fare.** Nessuna fonte dà un edge per trade alla pagina.

## Cosa la ucciderebbe, e la soglia della misura

**Soglia, uguale ai minimi del perimetro.** La misura deve passare **tutte e due** le condizioni.
- **Eccesso sul caso ≥ 3,0 errori standard** nell'in-sample 2020-2024. Con circa 232 trade un errore
  standard sul win rate vale circa 3,3 punti percentuali: servono circa 10 punti di eccesso.
- **$ al giorno per micro ≥ 10,0**, cioè circa 11 punti ES netti di media per lunedì (sezione 6).

**La soglia della SPEC qui non vale.** La SPEC di Mario usa quella della via B (t > 1,03 per
k = 4), che sta sotto il perimetro: vale la soglia del perimetro.

**Cosa la ucciderebbe, oltre la soglia**
- **Numero di trade.** Se non torna con il controllo di calendario (232, al più due in meno), è un
  errore della regola nel motore, non un risultato. Prima si corregge, poi si misura.
- **Concentrazione per anno.** Se il profilo per anno mostra che il risultato viene da un anno
  solo, il dossier lo deve dire anche se la misura passa. Un effetto di calendario vero non
  dovrebbe vivere su un anno.
- **Trade peggiore.** La regola della via B di Mario dice che una perdita oltre i 90 punti (oltre
  $500 per micro, anche per un gap) è un kill. Non è un criterio della misura, ma va stampato nel
  dossier.

**Perché secondo me non regge.** La porta è `user`: non cambio l'idea, lo scrivo qui.

1. **Il minimo in dollari, per costruzione.** A un trade a settimana servono circa 11 punti netti
   per lunedì, cioè i soli lunedì dovrebbero rendere quanto l'intero rialzo dell'indice nei cinque
   anni.
2. **L'eccesso sul caso non separa «lunedì» da «long ES per 21 ore».** In un periodo in cui ES sale,
   un long tenuto a lungo vince più spesso di un random walk. Una misura sopra soglia non
   dimostrerebbe un effetto del lunedì.
   - Il confronto giusto sarebbe lo stesso trade negli altri giorni della settimana.
   - Ogni misura conta: sarebbe un'idea nuova nel totale (la SPEC la chiama un gemello, k = 5), e
     la decide il desk.
3. **Metà del trade è overnight drift**, morto dopo il 2021 secondo i suoi autori.
4. **L'autore ha scelto la finestra con una ricerca sugli orari**, con un numero di prove che non
   conosciamo, e scrive da solo che l'effetto decade.
   - Il nostro 2020-2023 sta con ogni probabilità dentro il periodo su cui l'ha scelta. Lì una
     misura sopra soglia è in parte attesa per costruzione.
   - Il nostro 2024 sta dentro il suo OOS, dove secondo la trascrizione il 2024 è «quasi piatto».
5. **Chi perde non è stabilito.**

**Questa soglia non è scritta alla cieca.** Il desk mi ha detto che sulla strategia non esiste
alcun numero, ma `fonti/idea.md` (la SPEC del 10/11/2026, sezione «Contaminazione») dice un'altra
cosa:
- riporta una misura del desk sull'in-sample 2020-2024, su ES a 1 minuto, della stessa regola senza
  stop e con i lunedì festivi compresi: trade, WR, media per trade, t e profilo per anno;
- dice che anche le tre versioni con filtro dell'autore sono state guardate su dati proxy (k = 4).

Quei numeri li ho letti. Non li ho usati né come attesa né per la soglia, che viene dal perimetro e
dal calendario. Questa misura entra nel registro come uno sguardo in più sugli stessi dati, non
come il primo.

---

Altre ipotesi nella stessa fonte, una riga ciascuna. Secondo la SPEC sono tutte già state guardate
su dati proxy:
- L644ES: lo stesso long del lunedì su ES con il filtro sulla distanza dalla EMA, senza stop.
- L656ES: long del lunedì su ES solo dopo un venerdì in rialzo.
- L644NQ: long del lunedì su NQ con il filtro ADX.
