# alta_frequenza_sharpe

## Ipotesi

**Esito del ricercatore: non c'è un'ipotesi difendibile per questo tema.** Il file non propone una
regola da codificare. Spiega con l'aritmetica perché il vincolo di progetto (pass in 5-10 giorni)
richiede una qualità del segnale che né la letteratura né il cimitero hanno mai mostrato, e
pre-registra la soglia che qualunque idea futura con questo vincolo di progetto dovrebbe superare.
Non è una variante di un'idea morta: non c'è un'idea.

L'ipotesi che il tema chiede, «esiste su NQ/ES un segnale intraday da molti trade al giorno il cui
Sharpe giornaliero netto basta a passare la LucidFlex 50k in 5-10 giorni», è falsificabile, ma non
ho trovato niente che la renda plausibile. Scritta in forma misurabile (sezione 7) richiede
sull'IS 2020-2024 un t di almeno 8, contro il 3,03 dell'unica sopravvissuta.

## Meccanismo

Non ne ho uno che produca molti segnali al giorno con edge lordo sopra i costi. I flussi
obbligati noti sugli indici USA sono pochi e legati a orari (chiusura, ribilanciamenti, roll,
annunci): danno al massimo uno o due segnali al giorno, e quelli intraday pubblicati con
campione pre-2021 sono morti (LastHalfHour, overnight drift, FX Fix).

L'unico flusso obbligato che agisce molte volte al giorno è il ribilanciamento delta dei market
maker sulle opzioni S&P, che con le 0DTE pesa di più. Una sintesi di Quantpedia riporta che, quando
il gamma netto dei market maker è più alto, il flusso di ordini sull'E-mini mostra reversal più
forti e i rendimenti ad alta frequenza hanno momentum negativo, con un effetto che si dissolve in
circa un'ora. Su questo pesano tre problemi:
- è mean reversion a orizzonte corto come strategia autonoma, una famiglia esclusa con una madre
  morta (VWAP Fade);
- richiede di sapere il segno del gamma dei dealer. `desk_ricerca.md` dice che il GEX è nel lake,
  `prompt_ricerca_strategie.md` dice che non lo abbiamo, e il motore misura solo barre da 1
  minuto: il filtro 9 non è stabilito;
- la stessa sintesi dice che l'hedging ad alta frequenza di un portafoglio lungo gamma è
  profittevole in media solo «quando i costi di transazione sono bassi», cioè per chi fa il
  market maker, non per noi a $2,50 a giro.

## Chi perde, e perché continua a perdere

Non lo so nominare. A molti trade al giorno su un contratto liquidissimo, dall'altra parte ci sono
soprattutto market maker e algoritmi a bassa latenza, che pagano meno di noi e vedono il book. Non
c'è un perdente strutturale che io sappia indicare e che noi, su barre da 1 minuto e con
$2,50 a giro per micro, potremmo battere. Secondo le regole del desk questo basta a uccidere
l'idea.

## Fonti

Tipo: **idea propria**. Nessuna fonte misura un effetto con queste caratteristiche, e nessun numero
esterno entra nell'aritmetica di questo file.

- Ricerca web del 17/11/2026 (una ricerca estesa e una standard): nessun backtest credibile di un
  edge intraday frequente su ES/NQ, con campione oltre il 2021, che sopravviva ai costi retail.
  Conferma la ricerca del 18/10.
- Adams et al., *Do S&P500 Options Increase Market Volatility? Evidence from 0DTEs*, letto solo
  nella sintesi di Quantpedia («Do S&P500 0DTEs Options Increase Market Volatility?», pagina
  aperta il 17/11/2026), non nel paper.
  - Anno e rivista: non stabiliti.
  - Cosa dice la sintesi: un gamma netto più alto dei market maker predice reversal più forti nel
    flusso di ordini dell'E-mini e momentum negativo nei rendimenti ad alta frequenza; l'effetto
    si dissolve in circa un'ora; l'hedging è profittevole in media se i costi sono bassi.
  - Nessuna pagina del paper, nessun numero di effetto: non entra in nessun conto.
- Baltussen, Da, Soebhag, *End-of-Day Reversal* (working paper, `academicweb.nd.edu/~zda/EOD.pdf`):
  non ho potuto aprire le pagine (PDF non leggibile da qui), quindi nessun numero. Lo cito solo
  come pista. Che sia circa un segnale al giorno, nella parte finale della sessione, è dedotto
  dal titolo e non verificato.
- Numeri interni usati nell'aritmetica, senza pagina perché documenti del laboratorio:
  - DriftPullback: eccesso +2,8 pp, 3,2 trade al giorno, $18,34 al giorno per micro e 42% di
    pass per tentativo allo Stage 7 (`cosa_uccide_le_strategie.md`); t 3,03 sull'IS
    (`desk_ricerca.md`, «La misura preliminare»);
  - massimo eccesso mai visto: +5,3 pp (VaultBreak, a 0,6 trade al giorno);
  - regole LucidFlex: `prompt_ricerca_strategie.md`.

## Regola eseguibile

Nessuna: il coder non ha niente da scrivere. Non metto in forma una regola che non so difendere
solo per avere qualcosa da misurare. Ogni misura conta nel tetto di 8 idee al mese e nel registro
dei tentativi.

## Frequenza e costi

**Costo di un trade.** Commissione di $1,50 a round-turn per micro, più uno slippage dichiarato
di 1 tick per lato, che è una scelta ottimista per ingressi a mercato o stop in un sistema che
opera tutto il giorno:
- MNQ: $1,50 + 2 × $0,50 = **$2,50**, cioè 1,25 punti NQ;
- MES: $1,50 + 2 × $1,25 = **$4,00**, cioè 0,8 punti ES.

Il pavimento di `prompt_ricerca_strategie.md` (edge lordo di almeno 3 volte il costo) chiede quindi
**≥ 3,75 punti NQ lordi a trade** (≥ 2,4 su ES).

**Cosa chiede il pass in 5-10 giorni.** Lo tratto come un moto browniano con deriva μ e
volatilità σ al giorno, tra le barriere +$3.000 e −$2.000. È un'approssimazione ottimista: ignora
il trailing EOD, che stringe la barriera bassa dopo i giorni buoni, e la consistency al 40%, che
impone almeno 3 giorni positivi.

- P(pass) = (e^{4x/3} − 1) / (e^{4x/3} − e^{−2x}), con x = S²·N, S = μ/σ lo Sharpe giornaliero e
  N = 3.000/μ i giorni attesi al target.
- Senza edge (x → 0), P(pass) = 2/5 = 40%.

| P(pass) voluta | x | S giorno, N=10 | S giorno, N=5 | S annuo (N=10 / N=5) |
|---|---|---|---|---|
| 60% | 0,50 | 0,22 | 0,32 | 3,5 / 5,0 |
| 80% | 1,15 | 0,34 | 0,48 | 5,4 / 7,6 |

**Tradotto nella misura.** Con trade indipendenti, il t sui trade dell'IS è circa S·√D, con
D ≈ 1.250 giorni di borsa nel 2020-2024 (√D ≈ 35,4).
- Per il 60% in 10 giorni serve **t ≈ 8**; per l'80% in 10 giorni **t ≈ 12**; per l'80% in 5
  giorni **t ≈ 17**.
- DriftPullback, la migliore mai misurata qui, ha t 3,03, cioè S ≈ 0,085 al giorno.

A DriftPullback non manca la media. $18,34 per micro × 40 micro fanno circa $730 al giorno, cioè
4 giorni sul valore atteso. Manca lo Sharpe: con S ≈ 0,085 e N ≈ 4, x ≈ 0,03 e la formula dà
P(pass) ≈ 41%, quasi il 40% del caso. Il vincolo che lega è la varianza giornaliera, non i dollari
al giorno.

**Calibrazione dell'approssimazione.** Il simulatore dello Stage 7 ha dato a DriftPullback il 42%
per tentativo (`cosa_uccide_le_strategie.md`); la formula dà circa il 41%. Non conosco la size né
l'orizzonte usati dal simulatore, quindi è un accordo indicativo, non una prova. Basta però a dire
che la soglia t ≥ 8 non è un artificio del modello.

**Perché la frequenza da sola non risolve: frequenza e costi si contraddicono.** Per un bracket
con eccesso e sul caso (win rate vicino al 50%), lo Sharpe lordo per trade è circa 2e, quindi
servono n = S²/(4e²) trade indipendenti al giorno.
- Il pavimento sui costi chiede un bracket largo W = stop + target ≥ 3c/e.
- In un random walk un bracket simmetrico largo W dura in media (W/2)²/σ₁² minuti, dove σ₁ è la
  deviazione standard a 1 minuto. NQ RTH: σ₁ ≈ 10 punti [stima: circa 200 punti di deviazione
  giornaliera RTH / √390, non misurata sull'IS].
- Imponendo che gli n trade stiano nei 390 minuti RTH, anche stando a mercato tutto il tempo:
  e ≥ (9·S²·c² / (16·390·σ₁²))^¼.
- Con c = 1,25 punti:

| obiettivo | eccesso minimo su ogni trade | trade indipendenti al giorno | durata media |
|---|---|---|---|
| 60% in 10 giorni (S = 0,22) | ≈ 3,3 pp | ≈ 11 | ≈ 35 min |
| 80% in 10 giorni (S = 0,34) | ≈ 4,0 pp | ≈ 18 | ≈ 22 min |
| 80% in 5 giorni (S = 0,48) | ≈ 4,8 pp | ≈ 25 | ≈ 15 min |

  Tutte le righe richiedono di stare a mercato per l'intera sessione.

Il risultato dipende da σ₁ solo con la radice quarta: con σ₁ = 8 punti gli eccessi salgono
dell'11%. È sempre sopra il +2,8 della sopravvissuta, a una frequenza 3-8 volte più alta, e vicino
al +5,3 visto una sola volta, a 0,6 trade al giorno, e poi morto fuori campione. Senza il
pavimento 3× (edge lordo appena sopra il costo) l'eccesso richiesto scende di circa √3, ma il
netto per trade va a zero e lo Sharpe netto con lui.

Su MES va peggio. L'eccesso richiesto scala come √(c/σ₁):
- NQ: 1,25/10;
- ES: 0,8/2,8, con σ₁ di ES ≈ 2,8 punti [stima, non misurata].

Su MES serve quindi circa il 50% di eccesso in più che su MNQ. E lo stesso segnale su un indice
correlato non è diversificazione.

**Segnali al giorno attesi da una proposta difendibile: nessuna proposta.** Una che rispettasse il
vincolo dovrebbe farne 11-25 indipendenti al giorno.

## Cosa la ucciderebbe, e la soglia della misura

Scritta ora, prima di qualsiasi numero. Vale per qualunque idea futura con questo vincolo di
progetto.

- Minimi della destinazione `prop` (`perimetro.yaml`): eccesso/errore standard ≥ 3 e ≥ $10 al
  giorno per micro.
- **Soglia di questa idea, più severa e derivata dal vincolo:** t ≥ 8 sull'IS 2020-2024 (60% di
  pass in 10 giorni, nell'approssimazione ottimista della sezione 6), ≥ 5 setup al giorno di
  media (scelta: sopra i 3,2 di DriftPullback, altrimenti non è «alta frequenza») e ≥ $10 al
  giorno per micro al netto di $2,50 a giro per micro su MNQ ($4,00 su MES).
- Sotto t 8 la regola può essere una buona strategia, ma non risponde a questo tema e va
  registrata come idea diversa.
- La ucciderebbe anche un eccesso sul caso che c'è ma sparisce nella seconda metà dell'IS
  (2022-2024, l'era 0DTE). Gli effetti intraday sugli indici sono morti proprio lì.

Perché secondo me il tema non regge. Il vincolo «pass in 5-10 giorni» è un vincolo sullo Sharpe
giornaliero (3,5-7,6 annuo), non sulla frequenza. La frequenza aiuta solo se ogni trade porta un
eccesso che non abbiamo mai visto. Con barre da 1 minuto e costi retail, Sharpe di quell'ordine
sono il territorio di chi fa market making con il book, non nostro. La leva sui giorni al pass,
con quello che c'è oggi, mi sembra la size e la gestione del rischio sulla strategia viva, che è
il lavoro del simulatore dello Stage 7, non una strategia nuova. È un'osservazione, non
un'ipotesi.

Altre piste viste, una riga ciascuna, per il desk:
- Reversal intraday condizionata al gamma dei market maker (Adams et al., letto solo nella sintesi
  Quantpedia): l'unico flusso obbligato ad alta frequenza, ma è mean reversion autonoma (madre
  VWAP Fade), il filtro 9 non è stabilito (GEX nel lake, il motore non lo legge) e la fonte la dice
  profittevole solo con costi bassi.
- End-of-Day Reversal (Baltussen, Da, Soebhag): dal titolo, circa 1 segnale al giorno nella parte
  finale della sessione, vicino a LastHalfHour (cimitero), numeri non verificati sulla pagina.
  Fuori tema per la frequenza.
