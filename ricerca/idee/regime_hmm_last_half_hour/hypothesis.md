# regime_hmm_last_half_hour

**Variante di un'idea già morta.** La madre è **LastHalfHour** (Baltussen, Da, Lammers, Martens,
JFE 2021), chiusa. `multicharts/docs/come_scegliere_un_paper.md` riporta che è morta dopo maggio
2020 e la usa come caso della domanda 8. Questa idea non cambia il trade della madre: le
aggiunge un filtro di regime. Porta `user`: l'idea è di Mario, qui è solo messa in forma. Le
mie riserve stanno nella sezione 7.

## Ipotesi

Su @NQ, nei giorni in cui un HMM a 2 stati stimato fino alla chiusura del giorno prima assegna
più del 50% di probabilità allo stato «rischioso», il rendimento 14:30-15:00 CT ha lo stesso
segno del rendimento che va dalla chiusura RTH di ieri alle 14:30 di oggi. Sul 2020-2024 questo
basta a superare 3 errori standard e 10 dollari al giorno per micro. Se il filtro non porta la
misura sopra queste soglie, l'ipotesi è falsa.

## Meccanismo

- **Il flusso, dal paper.** I market maker di opzioni coprono il delta. Quando sono corti di
  gamma, la copertura li obbliga a comprare dopo un rialzo e a vendere dopo un ribasso, e gran
  parte di questo ribilanciamento cade verso la chiusura. Il risultato è che il movimento della
  giornata continua nell'ultima mezz'ora. Il paper lo misura condizionando sul segno del gamma
  netto dei market maker: con gamma negativo l'effetto è forte, con gamma non negativo non è
  significativo (fonte 1, pp. 388-389).
- **Il passaggio al regime: idea propria, debole.** Mario sostiene che nei regimi turbolenti i
  dealer siano più spesso corti di gamma, e che quindi lo stato rischioso dell'HMM approssimi i
  giorni con gamma negativo. **Nessuna delle fonti che ho aperto lo dimostra sull'indice.** Il
  paper madre non lega il segno del gamma a ribassi o crisi. Dice anzi che, dal 1996 a maggio
  2020, i giorni con gamma negativo sono circa la metà (fonte 1, pp. 388-389), e in nota che il
  gamma netto è in media positivo. L'argomento meccanico esiste: i dealer sono considerati corti
  di put, e quando l'indice scende verso i loro strike il gamma corto cresce. Ma è un argomento,
  non una misura.
- **L'appoggio indiretto, con le sue differenze.** Gao, Han, Li, Zhou (fonte 2) trovano che il
  momentum dell'ultima mezz'ora cresce con la volatilità. Ci sono però tre differenze dalla
  nostra regola:
  - la volatilità che usano è quella della prima mezz'ora dello **stesso giorno**, divisa in
    terzili, e non un regime stimato ieri;
  - lo strumento è SPY, non un future;
  - il campione è 1993-2013.
- **L'HMM.** Un modello a due stati sui rendimenti azionari separa di solito un regime a
  volatilità alta con rendimento medio basso da uno calmo (fonte 3, p. 13). Per questo «stato
  con la media più bassa» dovrebbe coincidere quasi sempre con «stato turbolento».

## Chi perde, e perché continua a perdere

- **Chi paga la continuazione** è chi deve coprirsi a qualunque prezzo vicino alla chiusura:
  i market maker di opzioni corti di gamma e, secondo il paper madre, gli ETF a leva che
  ribilanciano a fine giornata. Non smettono perché il loro mandato è restare delta-neutrali,
  non guadagnare su quella mezz'ora.
- **Il punto debole.** Il paper madre mostra il flusso fino a maggio 2020. Dopo il 2021 le
  opzioni 0DTE hanno cambiato il posizionamento dei dealer, e la nota del lab attribuisce a
  questo la morte degli effetti intraday sugli indici. Che il flusso di copertura nei giorni
  turbolenti dopo il 2021 vada ancora nella direzione del momentum: **non lo so, e non ho una
  fonte che lo dica.**

## Fonti

**Tipo: `paper` per l'effetto di base (l'ultima mezz'ora); `idea propria` per il filtro HMM e
per il legame tra regime e gamma.** Nessuna fonte misura l'effetto con questo filtro. Il critico
deve leggere il filtro con le regole di un'idea propria, quindi come un parametro in più senza
prove.

1. **Baltussen, G., Da, Z., Lammers, S., Martens, M. (2021), «Hedging demand and market intraday
   momentum», *Journal of Financial Economics* 142, 377-403.** Ho letto la versione pubblicata,
   ospitata dall'autore: https://academicweb.nd.edu/~zda/intramom.pdf
   - p. 380: il campione va da dicembre 1974 a maggio 2020 e comprende 62 futures, di cui 17 su
     indici azionari.
   - p. 385: la strategia prende ogni giorno il rendimento dell'ultima mezz'ora con il segno
     del rendimento fino a 30 minuti prima della chiusura. Gli autori scrivono che non
     considerano i costi di transazione. Aggiungono che sui futures S&P 500 lo Sharpe resta
     positivo con un costo di un tick, ma non danno il numero.
   - p. 386, Tabella 6, futures su indici azionari (portafoglio 1/N), strategia η(rROD):
     rendimento annualizzato 6,86%, deviazione standard 3,96%, Sharpe 1,73, quota di giorni
     giusti 0,55. Lordo, senza scaling di volatilità.
   - pp. 388-389, Tabella 7, futures S&P 500, gamma netto dei market maker misurato il giorno
     prima:
     - con gamma negativo, βROD = 6,63 (t 4,78), R² 3,58%;
     - con gamma non negativo, βROD = 0,82 (t 1,03), R² 0,05%.
     
     Il testo dice che il momentum intraday è «molto più pronunciato» nei giorni con gamma
     negativo.
   - Tabella 8, colonna 1 (pp. 388-389): sul campione con il gamma (1996-2020), futures S&P
     500, βROD = 5,08 (t 4,72), R² 2,32%.
   - pp. 388-389: dal 1996 a maggio 2020 ci sono 2.930 giorni con gamma netto negativo e 3.158
     con gamma positivo. In nota dice che il gamma netto è in media positivo. Il paper **non**
     collega il segno del gamma a ribassi, crisi o volatilità alta.
   - **Sulle pagine.** Ho letto il PDF come testo estratto. L'estrazione non fissa con certezza
     il salto fra p. 388 e p. 389: la frase «molto più pronunciato» è con buona probabilità a
     p. 388, le Tabelle 7 e 8 a p. 388 o 389. Il critico verifichi sul PDF.
   - **Filtro 8:** il campione finisce prima del 2021. Per l'effetto **condizionato** dopo il
     2021 non ho trovato un lavoro che si possa verificare a una pagina. Adams et al. (SSRN
     5641974, 2026) è citato nella nota interna `ricerca_gamma_0dte.md`, ma non l'ho aperto e
     non ne riporto numeri.

2. **Gao, L., Han, Y., Li, S. Z., Zhou, G. (2015, working paper, versione di dicembre 2015),
   «Intraday Momentum: The First Half-Hour Return Predicts the Last Half-Hour Return».** Il
   paper è uscito come «Market intraday momentum», *JFE* 129 (2018), 394-414, ma io ho aperto
   il working paper e le pagine sono quelle:
   https://c.mql5.com/forextsd/forum/173/intraday_momentum_-_the_first_half-hour_return_predicts_the_last_half-hour_return.pdf
   - p. 3: la volatilità è quella realizzata, calcolata sui rendimenti a 1 minuto della prima
     mezz'ora.
   - p. 6: i giorni sono divisi in terzili di quella volatilità. Gli autori scrivono che la
     prevedibilità sembra crescere con la volatilità.
   - p. 31, Tabella 3, pannello A: R² 0,6% nel terzile basso, con coefficiente non
     significativo; 1,0% in quello medio; 3,3% in quello alto. Il campione è SPY dal 1993 al
     2013.
   - **Cosa non dice:** niente su un regime stimato il giorno prima, niente sui futures, niente
     dopo il 2013.

3. **Ang, A., Timmermann, A. (2011), «Regime Changes and Financial Markets», NBER Working Paper
   17182** (poi in *Annual Review of Financial Economics* 4, 2012; le pagine sono quelle del
   working paper): https://www.nber.org/system/files/working_papers/w17182/w17182.pdf
   - p. 2: i modelli a regimi ricorrenti sono stati usati per descrivere mercati rialzisti e
     ribassisti, calmi e turbolenti.
   - p. 13: sulle azioni c'è un regime ad alta volatilità che in media ha rendimenti bassi, e
     corrisponde ai mercati ribassisti.
   - p. 14: i regimi sono persistenti, con probabilità di permanenza vicine a uno. Nello stesso
     modello, però, il 1997-2003 cade nel regime ad alta volatilità pur contenendo il rialzo di
     fine anni '90. Quindi «media bassa» e «volatilità alta» non coincidono sempre.
   - p. 11: tracciare il regime in tempo reale è difficile. p. 12: stimare le medie dei
     rendimenti è difficile anche senza regimi. p. 14: la prevedibilità soffre di rotture e di
     instabilità dei parametri.

**Senza fonte, quindi deboli:**
- che lo stato rischioso dell'HMM coincida con il gamma negativo dei dealer;
- la finestra di 504 giorni, la volatilità a 20 giorni e i due stati (sono scelte di Mario);
- che l'effetto condizionato sia vivo dopo il 2021.

Il video da cui nasce l'idea non è una fonte e non è citato.

## Regola eseguibile

**Il trade è quello della madre, senza modifiche.**
- Mercato @NQ (continuo back-adjusted del lake, `quantlake/data/multicharts/NQ_1min.csv`, dal
  03/01/2016), barre da 1 minuto. Orari in CT (= ET − 1 ora, con l'ora legale della borsa).
- **Chiusura RTH** del giorno d (C_d): close dell'ultima barra a 1 minuto della sessione RTH di
  d che termina alle 15:00 CT o prima. Nei giorni normali è la barra che termina alle 15:00;
  nei giorni a chiusura anticipata è l'ultima barra RTH.
- **Segnale** del giorno d: S = close della barra che termina alle 14:30 CT di d, meno C del
  giorno di borsa precedente (che può essere un giorno a chiusura anticipata). Conta solo il
  segno. Se S = 0, quel giorno non si opera.
- **Ingresso:** ordine a mercato all'apertura della barra delle 14:30 CT (cioè dopo la chiusura
  della barra che termina alle 14:30), long se S > 0, short se S < 0.
- **Uscita:** a mercato sulla chiusura della barra che termina alle 15:00 CT.
- **Niente stop e niente target**, come nel paper. Un tetto di rischio sarebbe un parametro in
  più che nessuna fonte giustifica. La perdita massima resta quella di una mezz'ora.
- **Massimo 1 trade al giorno.**
- **Giorni a chiusura anticipata** (sessione RTH che finisce prima delle 15:00 CT): non si
  opera. È una scelta dichiarata: la regola è definita sulla mezz'ora 14:30-15:00, e su quei
  giorni non esiste. Restano però nella serie dei rendimenti dell'HMM, e la loro C fa da
  chiusura precedente per il segnale del giorno dopo.
- Se in un giorno normale manca la barra delle 14:30 o quella delle 15:00, quel giorno non si
  opera.

**Il filtro.** È una serie giornaliera calcolata **fuori dalla strategia**, dopo la chiusura
RTH di d−1, e letta dalla strategia come dato. Si opera il giorno d solo se P_d ≥ 0,5.
Per ogni giorno di borsa d:

1. **Rendimento giornaliero.** r_t = C_t / C_{t−1} − 1, dove C è la chiusura RTH definita sopra
   sul continuo back-adjusted.
   - È una scelta dichiarata, ed è sbagliata in modo noto: il back-adjust additivo comprime i
     rendimenti percentuali di un fattore (prezzo vero / prezzo aggiustato) che cambia piano
     nel tempo.
   - I rendimenti in punti sarebbero peggio: NQ va da circa 4.500 a oltre 20.000 dal 2016 al
     2024, e la scala dei punti cambia molto più di quel fattore.
   - Dentro una finestra di 504 giorni la distorsione è un cambio di scala lento, uguale per i
     due stati.
2. **Volatilità realizzata.** v_t = deviazione standard campionaria (n−1) di r_{t−19}, …, r_t
   (20 rendimenti). Non annualizzata.
3. **Osservazione** del giorno t: il vettore x_t = (r_t, v_t).
4. **Finestra di allenamento** per il giorno d: gli ultimi 504 giorni di borsa che finiscono
   con d−1 compreso. Nessun dato del giorno d.
5. **Modello.** HMM a 2 stati, emissione gaussiana bivariata con **covarianza piena**, stimato
   con EM (Baum-Welch).
   - Le variabili si standardizzano con media e deviazione standard **della finestra** (z-score
     per colonna), così le due colonne hanno la stessa scala.
   - Inizializzazione: k-means con 2 cluster sugli z-score. 10 avvii, seme fisso 0; si tiene la
     soluzione con la log-verosimiglianza più alta.
   - Tolleranza 1e-4, massimo 1.000 iterazioni.
   - Distribuzione iniziale e matrice di transizione stimate, senza vincoli.
6. **Etichetta.** Lo stato rischioso è quello con la **media della componente r più bassa**
   nella finestra (regola di Mario). La media si confronta sulla scala originale; la
   standardizzazione non cambia l'ordine.
7. **Probabilità.**
   - Probabilità **filtrata** dello stato rischioso al giorno d−1, con l'algoritmo forward
     sulla finestra. All'ultimo punto della finestra filtrata e smussata coincidono, quindi non
     c'è dato futuro.
   - Probabilità **prevista** per d: P_d = f·a_RR + (1 − f)·a_CR, dove f è la filtrata in d−1,
     a_RR la probabilità di restare nello stato rischioso e a_CR quella di passare dallo stato
     calmo al rischioso.
8. **Soglia: P_d ≥ 0,5.** È il confine di decisione di un modello a due stati: si opera quando
   il modello stesso giudica il regime rischioso più probabile dell'altro. È l'unico valore che
   non richiede di guardare i dati. 0,7 o 0,9 sarebbero numeri scelti, e nessuna fonte ne dà
   uno.
9. **Riscaldamento.** Il primo P_d esiste quando ci sono 504 + 20 giorni di rendimenti, quindi
   circa da febbraio 2018 con i dati dal 2016. I giorni 2016-2019 servono solo a stimare, e
   non entrano nella misura. **Se il motore non riesce a leggere i dati prima del 2020, la
   misura non è valida.** Non va eseguita sul periodo che resta (il primo trade cadrebbe a
   inizio 2022 e il 2020 andrebbe perso del tutto).
10. **Il complemento esce dalla stessa esecuzione.** Il coder calcola P_d per ogni giorno in cui
    la madre avrebbe un segnale. Opera i giorni con P_d ≥ 0,5. Gli altri li registra come
    trade ombra, con la stessa regola, nella stessa misura. Non è una seconda misura.

**Gradi di libertà fissati, ciascuno una scelta libera che nessuna fonte giustifica:**

| | valore | da dove viene |
|---|---|---|
| numero di stati | 2 | Mario |
| finestra di allenamento | 504 giorni | Mario |
| finestra della volatilità | 20 giorni | Mario |
| variabili | r e v a 20 giorni | Mario |
| etichetta dello stato rischioso | media di r più bassa | Mario |
| soglia | 0,5 | io: confine di decisione |
| covarianza | piena | io |
| standardizzazione | z-score sulla finestra | io |
| inizializzazione EM | k-means, 10 avvii, seme 0 | io |
| tolleranza e iterazioni | 1e-4, 1.000 | io |
| giorni a chiusura anticipata | non operati, tenuti nella serie | io |
| definizione del rendimento | percentuale sul back-adjusted | io |

Sono **12 scelte**. Nessuna va variata dopo aver visto la misura. Il critico deve contarle come
gradi di libertà del ricercatore, anche se sono fissati prima.

## Frequenza e costi

- **Senza filtro**, la madre opera circa 1 volta al giorno: tutti i giorni RTH tranne quelli
  con S = 0 e quelli a chiusura anticipata. Nel 2020-2024 sono circa 1.250 giorni.
- **Con il filtro.** Non so a priori quanti giorni del 2020-2024 cadano nello stato rischioso,
  e non devo guardarlo. Il mio prior è fra il 25% e il 40%, perché il regime ad alta volatilità
  è di solito quello minoritario. Quindi **0,25-0,40 segnali al giorno, circa 300-500 trade**.
  Il filtro taglia il 60-75% dei trade.
- **Cosa significa per la potenza.** Con N trade, t ≥ 3 richiede un rapporto media/deviazione
  standard per trade di almeno 3/√N: 0,13 con 500 trade, 0,17 con 300 trade. Il paper, sul
  portafoglio di futures azionari, ha uno Sharpe annuo di 1,73 (p. 386), cioè circa 0,11 per
  giorno. È il mio conto: 1,73/√252. Ed è un portafoglio diversificato prima del 2020, quindi un
  limite alto per un mercato solo. **Anche con l'effetto pieno del paper, 400 trade danno t
  intorno a 2,2.** Per passare, il filtro deve far crescere l'effetto per trade di almeno una
  volta e mezza rispetto alla madre al suo meglio. Il paper fa qualcosa di simile solo con il
  gamma osservato (Tabella 7 contro Tabella 8, pp. 388-389: R² 3,58% contro 2,32%), non con un
  regime.
- **Dollari al giorno.** Anche qui il conto è mio.
  - Effetto lordo: 6,86% annuo / 252 ≈ 2,7 punti base per trade (p. 386, lordo, prima del
    2020). Con NQ fra 15.000 e 20.000 sono **circa 4-5 punti**, cioè **8-11 dollari per trade
    per micro** (MNQ, 2 dollari a punto).
  - Per 10 dollari al giorno con 0,25-0,40 trade al giorno servono **25-40 dollari netti per
    trade per micro, cioè 13-20 punti**: 3-5 volte l'effetto medio del paper.
  - Nei giorni turbolenti i movimenti in punti sono più grandi, quindi una parte del divario
    potrebbe chiudersi da sola. Ma è una speranza, non una fonte.
- **Costi.** Un giro su MNQ costa circa 1 tick di slippage per lato (0,25 punti = 0,50 dollari)
  più la commissione, quindi intorno a 2 dollari. Va usato il costo del motore. Contro 8-11
  dollari lordi l'effetto del paper copre i costi. **Il problema non è il costo, è la soglia in
  dollari al giorno con meno di mezzo trade al giorno.**
- Per il filtro 5 è al massimo una seconda gamba (sotto 1 segnale al giorno).

## Cosa la ucciderebbe, e la soglia della misura

**Soglie, sul 2020-2024 con destinazione `prop`, tutte insieme:**

1. Eccesso sul caso / errore standard **≥ 3,0**.
2. **≥ 10 dollari al giorno per micro**, netti, calcolati sui giorni di borsa del periodo (non
   sui soli giorni operati).
3. **Almeno 250 trade.** Con meno, la stima è un'aneddotica del 2020 e del 2022.
4. **Senza il crollo del 2020.** Togliendo i trade dal 15/02/2020 al 31/05/2020 l'eccesso deve
   restare positivo con **t ≥ 2**. Il filtro peserà molto su quel periodo, che è anche l'unico
   in cui la madre mostrava qualcosa. Se il risultato sta tutto lì, l'idea è un evento, non un
   effetto.
5. **Il complemento va riportato accanto** (i trade ombra della regola, punto 10). È lo stesso
   trade nei giorni con P_d < 0,5. Se il complemento ha un eccesso uguale o più alto di quello
   dei giorni filtrati, il filtro non isola niente e l'idea muore anche se le soglie 1-2
   passassero per caso.

**Cosa la ucciderebbe, prima di vedere un numero:**

- **Il vincolo tecnico.** `prompt_ricerca_strategie.md` esclude i «modelli addestrati a
  runtime», e un HMM ristimato ogni giorno lo è. La regola sopra lo trasforma in una serie di
  dati precalcolata e deterministica, che PowerLanguage legge come un input. Se il desk non
  accetta una serie esterna come input, l'idea non è eseguibile così com'è.
- **Il filtro 8, eliminatorio.** Il paper dell'effetto finisce a maggio 2020, e non ho
  evidenza verificabile che l'effetto **condizionato** sia vivo dopo il 2021. La risposta è:
  no, o non stabilito. Il filtro HMM è proprio il tentativo di far rivivere un effetto
  dichiarato morto; il rischio è selezionare un sottoinsieme di giorni in cui il rumore è
  andato bene.
- **Il legame regime-gamma non ha fonte.** Il paper madre dice che il gamma negativo riguarda
  circa metà dei giorni (pp. 388-389) e non lo collega alle crisi. Se lo stato rischioso non
  coincide con il gamma negativo, il filtro sceglie i giorni per una ragione che il meccanismo
  non spiega.
- **L'HMM sarà quasi un filtro sulla volatilità a 20 giorni.** v_t è molto persistente, e una
  variabile persistente in un HMM gaussiano domina la stima degli stati. In pratica il filtro
  sarà vicino a «volatilità a 20 giorni sopra un livello relativo alla finestra», con 11
  manopole nascoste in più. E l'etichetta per media più bassa può scegliere a volte lo stato
  calmo (Ang e Timmermann, p. 14). Chiedo che la misura riporti la quota di finestre in cui lo
  stato rischioso **non** è anche quello con la volatilità media più alta: se supera il 10%,
  l'etichetta di Mario non sta isolando la turbolenza.
- **Il prior, scritto ora.** La madre è morta dopo il 2020, e il conto della sezione 6 chiede
  3-5 volte l'effetto del paper. **Mi aspetto che muoia sulla soglia dei 10 dollari al giorno,
  o su quella senza il 2020.**

**Altre ipotesi nella stessa fonte, una riga ciascuna, per il desk:**
- Filtro sul gamma osservato al posto dell'HMM: il trade della madre solo nei giorni con gamma
  netto negativo del giorno prima. È il condizionamento del paper (pp. 388-389). Due ostacoli:
  il filtro 8, e un conflitto fra documenti. `prompt_ricerca_strategie.md` esclude ogni
  condizione sul gamma dei dealer, mentre `desk_ricerca.md` dice che il lake ha il GEX. Il desk
  deve scioglierlo prima.
- Filtro sulla volatilità della prima mezz'ora dello stesso giorno, terzile alto (Gao et al.,
  p. 6 e p. 31): nessun modello, un solo parametro, quello della fonte.
- Filtro sul livello del VIX della chiusura precedente: il proxy di regime più semplice; serve
  una soglia da giustificare.
