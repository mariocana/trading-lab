# prova2_orb_breakout

Idea di Mario (porta `user`), messa in forma senza cambiarla: la regola base del corso, senza
le varianti dello Stage 4. Nessuna madre nota: la prova è alla cieca e `GIA_FATTO` non nomina
idee simili già morte.

## Ipotesi

Nei giorni in cui una barra da 5 minuti di NQ chiude sopra il massimo dei primi 30 minuti della
sessione cash (08:30-09:00 CT), il prezzo sale di una distanza pari alla larghezza fra ingresso
e minimo del range prima di tornare a quel minimo più spesso di quanto succede per caso. Un long
con stop al minimo del range, target 1R e uscita alle 14:00 CT guadagna quindi più del caso,
al netto dei costi. Se l'eccesso sul caso non si distingue da zero, l'ipotesi è falsa.

## Meccanismo

Quello che dichiara Mario:
- **Flussi che entrano solo dopo l'apertura cash.** Fondi e algoritmi con benchmark sulla
  sessione regolare (VWAP, TWAP, ordini al prezzo di sessione) eseguono dalle 08:30 CT in
  poi. Se il flusso della giornata è in acquisto, il prezzo esce dal range iniziale verso
  l'alto e continua a salire finché l'esecuzione non è finita.
- **Momentum intraday documentato.** Mario cita Gao, Han, Li e Zhou (*JFE* 2018) e Zarattini
  (2023).

Le due citazioni vanno lette con cautela. Gao et al. misurano un'altra cosa: il rendimento della
prima mezz'ora prevede quello dell'ultima. Questa regola invece esce alle 14:00 CT, prima
dell'ultima mezz'ora (14:30-15:00 CT). Zarattini e Aziz usano un range di 5 minuti, non di 30,
con target 10R e su QQQ.

Detto onestamente, non c'è un flusso obbligato nominabile con precisione. Gli ordini a
benchmark di sessione sono un flusso reale, ma niente obbliga a eseguirli nella direzione della
rottura del range. È un pattern di continuazione, cioè comportamentale. Secondo il filtro
(punto 3) vale meno di un flusso forzato.

## Chi perde, e perché continua a perdere

Per Mario è chi va contro l'apertura (chi «fade l'apertura»): vende la rottura del massimo
aspettandosi un ritorno dentro il range.

Perché continua a perdere: non lo so con precisione. Una lettura possibile: il fade
dell'apertura funziona nei giorni di range, che sono la maggioranza, quindi chi lo fa vede più
vittorie che sconfitte e non smette. Perderebbe sui giorni di trend, dove la perdita è più
grande. È un'ipotesi mia, senza una fonte che la misuri. Un altro candidato sono i market maker,
che forniscono liquidità alla rottura e la pagano come costo di selezione avversa. Anche questo
non ha una fonte. Va trattato come «non stabilito».

## Fonti

Tipo di fonte: **praticante** (un corso). Si legge con il filtro P1-P6.

1. **Il corso.** Lo cita Mario in `fonti/idea.md`, senza nome, autore né data della
   pubblicazione. Il materiale originale non è in `fonti/`, quindi non ho potuto controllarlo.
   Cosa dichiara, nelle parole di Mario: la strategia è «validata dal corso su NQ 2021-26», con
   **823 trade, win rate 58%, guadagno medio $183 a trade, profit factor 1,28**. Non sono
   dichiarati:
   - se il guadagno medio è al netto dei costi;
   - un out of sample separato dall'in-sample;
   - quanti parametri sono stati scelti sul periodo mostrato.

   Le note riportano anche che in una «live indipendente» l'ottimizzazione della durata del
   range su NQ ha il picco a 30-32 minuti e tiene out of sample. Fonte non nominata e non
   verificata: non la uso come prova.
2. **Zarattini e Aziz**, *Can Day Trading Really Be Profitable?*, working paper SSRN 4416622,
   aprile 2023, non referato (https://papers.ssrn.com/abstract=4416622). È la «Zarattini 2023»
   di Mario. Testa su QQQ e TQQQ, dal 2016 al 2023, un'altra regola: range dei primi 5 minuti,
   direzione della prima candela, target 10R. Non sono riuscito ad aprire il PDF per leggerne le
   pagine, quindi **nessun suo numero entra in questo file**. Conta solo come precedente della
   famiglia (opening range breakout su indice Nasdaq).
3. **Timon-pascal Krueger**, post sul blog di MQL5, 25/09/2026, *The opening-range breakout
   paper, replicated on five indices: gross reproduced, net zero*
   (https://www.mql5.com/en/blogs/post/776235). È una pagina web singola, senza numeri di
   pagina. Replica la regola di Zarattini-Aziz (5 minuti, 10R) su CFD di NQ, SPX, Dow, DAX e
   FTSE dal 2015 a giugno 2026. Su NQ:
   - **lordo**: +0,131 R a trade (t 2,9);
   - **netto**: +0,002 R (t 0,0), con un costo andata e ritorno di 2,5 punti, cioè il 6-12% del
     rischio a trade;
   - negli anni 2021-2026, al più +0,06 R.

   È un'altra regola, ma è l'unico controllo indipendente che ho trovato sulla famiglia. Dice
   che il lordo c'è ed è grande più o meno quanto il costo.

Gao, Han, Li e Zhou, *Market Intraday Momentum* (*JFE* 2018), è citato da Mario ma misura un
altro effetto (vedi Meccanismo). Non l'ho aperto e nessun suo numero entra.

## Regola eseguibile

Regola base del corso. Le scelte mie sono segnate come **[scelta]**, con il motivo.

- **Mercato.** NQ, contratto continuo (front month), con il roll standard del motore.
  Dimensione: 1 contratto. I dollari si riportano anche per un micro (MNQ = 1/10).
- **Timeframe e orario.** Barre da 5 minuti, ora di Chicago. **[scelta]** L'orario di una barra
  è quello di chiusura, come in MultiCharts: la barra «09:00» copre 08:55-09:00. Se il motore
  legge barre da 1 minuto, quelle da 5 si costruiscono aggregando cinque barre allineate
  all'ora piena (08:30-08:35, 08:35-08:40, …).
- **Giorni.** Tutte le sessioni cash del periodo che hanno la barra delle 08:35.
  **[scelta]** Senza quella barra il giorno si salta. Niente filtri per giorno della settimana,
  notizie o volatilità: il corso non li ha.
- **Range.** Le sei barre che chiudono dalle 08:35 alle 09:00 comprese. Il massimo del range è
  il massimo dei loro high, il minimo è il minimo dei loro low. Si usano solo barre della
  sessione cash: la notte Globex non conta.
- **Setup.** La prima barra che chiude dopo le 09:00 (dalla barra delle 09:05 in poi) con
  **chiusura strettamente sopra il massimo del range**. Conta solo il primo setup del giorno.
  Solo long: una chiusura sotto il minimo del range non fa niente.
- **Ingresso.** Ordine a mercato all'apertura della barra successiva al setup.
  **[scelta]** È la lettura più semplice di «prima barra che chiude sopra» in MultiCharts
  («buy next bar at market»).
- **Finestra degli ingressi.** Si accettano setup sulle barre che chiudono dalle 09:05 alle
  13:50 comprese. **[scelta]** Così l'ingresso cade al più tardi all'apertura della barra
  13:50-13:55, prima dell'uscita a tempo. Il taglio alle 11:00 è una variante dello Stage 4 e
  qui non c'è.
- **Stop.** Ordine stop al minimo del range, fisso, attivo dalla barra di ingresso.
- **Rischio R.** R = prezzo di ingresso effettivo − minimo del range. **[scelta]** Il prezzo di
  ingresso è il fill reale (apertura della barra dopo il setup), non la chiusura del setup.
  Così il bracket è simmetrico rispetto a dove si è davvero entrati. Se l'apertura della barra
  di ingresso è uguale o sotto il minimo del range (R ≤ 0), il trade non si apre e il giorno è
  chiuso.
- **Target.** Ordine limite a ingresso + 1 × R, fisso.
- **Stop e target nella stessa barra.** **[scelta]** Si assume che il prezzo abbia toccato
  prima lo stop. È la lettura prudente: con barre da 5 minuti non si sa quale sia venuto prima.
  Se il motore lavora a 1 minuto, vale la stessa regola sulla barra da 1 minuto.
- **Uscita a tempo.** Se il trade è ancora aperto, si chiude a mercato alla chiusura della barra
  delle 14:00 CT. Nelle sessioni accorciate (chiusura cash alle 12:00 CT) si chiude sull'ultima
  barra della sessione. **[scelta]** È il modo più semplice di restare flat entro la sessione.
- **Massimo di trade al giorno.** 1. Dopo uno stop, un target o l'uscita a tempo, non si
  rientra.
- **Parametri.** Nessuno libero. Range di 30 minuti, target 1R e uscita alle 14:00 sono del
  corso. Le scelte sopra sono di esecuzione, non di ottimizzazione, e non vanno variate.

## Frequenza e costi

- **Segnali al giorno: al massimo 1 per costruzione, circa 0,6 in media.** La stima viene dal
  corso: 823 trade su NQ dal 2021 al 2026, cioè circa 1.300-1.400 sessioni. Il conto è mio, sul
  numero dichiarato.
- **Effetto contro costo.** Il corso dichiara $183 medi a trade su NQ intero, circa 9 punti. Non
  dice se sono netti. Un costo andata e ritorno ragionevole (commissione più un tick di
  slippage per lato) sta intorno ai 0,5-1 punto. Se i $183 sono lordi, l'edge è circa 9-18
  volte il costo: P6 sarebbe soddisfatto. Per un micro, $18,3 a trade per 0,6 trade al giorno
  fanno circa **$11 al giorno**: appena sopra il minimo di $10 del perimetro, prima dei costi.
- **Avvertenza dalla fonte 3.** Sulla variante a 5 minuti il lordo su NQ era più o meno pari al
  costo. Con un range di 30 minuti lo stop è più lontano, quindi il costo pesa meno in R.
  Questo gioca a favore di questa versione, ma va misurato.

## Cosa la ucciderebbe, e la soglia della misura

Scritto prima di qualsiasi numero. Muore se succede una sola di queste cose sul periodo
in-sample 2020-01-01 → 2024-12-31:

1. **Eccesso sul caso / errore standard < 3,0**, al netto dei costi. È il minimo del perimetro,
   e lo tengo così.
2. **Meno di $10 al giorno per micro**, al netto. È il minimo del perimetro.
3. **Meno di 1 segnale al giorno.** È il minimo di `perimetro.yaml` per l'intraday. Lo segnalo
   adesso: **con un trade al giorno al massimo e circa 0,6 attesi, la regola di Mario
   probabilmente non raggiunge questo minimo per costruzione**, qualunque sia l'edge. Non ho
   cambiato la regola per farla passare (porta `user`). Se il desk applica il minimo alla
   lettera, l'idea muore qui. Il filtro dei paper (punto 5) ammette circa 1 al giorno solo per
   una seconda gamba.
4. **[più severo del perimetro]** L'eccesso è negativo in una delle due metà del periodo
   (2020-2022 e 2023-2024). Un effetto che vive solo nel 2020, l'anno dei trend estremi, non è
   un effetto.
5. **[più severo del perimetro]** L'eccesso sparisce contro un caso solo-long. È il rischio
   principale. Dal 2020 al 2024 NQ ha avuto una deriva rialzista forte, e una regola solo long
   con bracket simmetrico 1R ne approfitta anche senza nessuna informazione nella rottura. Il
   caso giusto è un long con lo stesso bracket, lo stesso orario di ingresso e la stessa
   frequenza, ma in giorni e momenti presi a caso. Se la misura confronta con un caso che ha
   long e short a metà, l'eccesso è gonfiato dalla deriva e va riletto.

Dove la vedo debole, prima della misura: niente flusso obbligato; nessun numero della fonte
verificabile a pagina; nessun out of sample dichiarato dal corso; la fonte indipendente (3) dice
che sulla variante a 5 minuti il netto è zero.

Altre ipotesi nella fonte. Sono le varianti dello Stage 4: il desk decide se aprirle come idee
nuove.
- Target 0,5R al posto di 1R.
- Ingressi solo fino alle 11:00 CT.
- Filtro sul delta della barra di rottura (UpTicks − DownTicks ≥ 200).
- Tetto al rischio in dollari (`MaxRisk_USD`).
- Gamba short, simmetrica sotto il minimo del range (atteso dal corso: non funziona).
- Ingresso su ritracciamento al VWAP ancorato alla rottura (1-1,5 deviazioni standard, stop
  2×ATR).
- Range di 60 minuti (Initial Balance), che il corso tratta come strategia separata.
