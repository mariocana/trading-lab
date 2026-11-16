# prova2_overnight_bias

Porta: user. Idea di Mario, messa in forma senza cambiarla. Il testo di partenza è in
`fonti/idea.md`. Nessuna madre nota: `GIA_FATTO` non ne nomina.

## Ipotesi

Su NQ, nei giorni in cui l'apertura delle 08:30 CT cade nel terzo alto del range della notte
(mezzanotte-08:30 CT), il breakout al rialzo dell'opening range dei primi 15 minuti prosegue
abbastanza da pagare un target pari a 3 volte lo stop più spesso di una volta su quattro. Nel
terzo basso vale lo stesso al ribasso. Se dal 2020 al 2024 questa regola non batte il caso con
t ≥ 3, l'ipotesi è falsa.

## Meccanismo

È l'argomento dell'autore. Il range della notte riassume il posizionamento di chi ha già
agito. Se il cash apre vicino a un estremo di quel range, l'apertura conferma quella
direzione, e il breakout dell'opening range nello stesso verso ha più probabilità di
diventare un movimento di trend che un falso breakout. I filtri servono a tenere fuori i
casi in cui questo non vale: ADX(16) ≥ 20 per avere trend, barra del segnale non più grande
di 2,5 volte la media per non entrare su un'esaurimento, giorno scartato se l'opening range è
più del doppio del normale.

Nessun flusso obbligato. È un pattern di momentum e di comportamento. Per i filtri del
critico pesa meno di un meccanismo di hedging o di ribilanciamento, e lo scrivo qui
apertamente.

## Chi perde, e perché continua a perdere

Secondo l'autore perde chi fada il breakout d'apertura nei giorni di trend, cioè chi vende
il massimo dell'opening range aspettandosi il ritorno nel range. Nelle giornate in laterale
quella scommessa paga spesso, e per questo chi la fa non smette. Perde nei giorni di trend,
che sono pochi ma grandi.

Non so nominare un soggetto più preciso di così: nessun flusso forzato, nessun partecipante
che sia obbligato a stare dall'altra parte. «Il fader dei giorni di trend» è una risposta
debole e la lascio debole.

## Fonti

Tipo di fonte: **praticante** (corso).

1. **Il corso «The Bridge», cartella «PROP FIRM NATIVE HIGH RR», file `Overnight Bias ORB.txt`
   (segnale `OFB_OvernightBiasORB_Signal`)**, unico file della cartella. Autore: chi ha
   scritto il corso, non nominato nel file per quanto riportato da Mario. Data del codice:
   non riportata. Mario l'ha trascritta il 29/10/2026 in `fonti/idea.md`. È codice
   PowerLanguage completo, con le regole già scritte.

   Cosa dichiara l'autore, nell'header del codice, a costi zero su 1 NQ (riportato da
   Mario; io non ho aperto il file originale):
   - in-sample 2006-2019: 1.112 trade, profit factor 1,35, net $50.445, drawdown $6.160;
   - out-of-sample 2020 → agosto 2026: 599 trade, profit factor 1,66, net $257.615, drawdown
     $20.195.

   Livello della fonte: **2**, testata senza costi. C'è una divisione IS/OOS dichiarata, ma
   non si sa quando il codice è stato scritto: se è del 2025-2026, il suo «OOS» è in-sample
   per l'autore. Il nostro periodo di misura (2020-2024) sta tutto dentro l'OOS dichiarato.
   Numero di parametri ottimizzati: non dichiarato.

   Conti miei sui numeri dell'autore (non sono della fonte): nell'OOS circa $430 lordi per
   trade per NQ, circa $43 per micro. Con un target a 3R, un profit factor di 1,66 implica una
   percentuale di trade vinti intorno al 36%, e un'aspettativa di circa 0,43 R per trade; con
   1,35 (2006-2019) circa 31% e 0,24 R.

Nessun paper: non ho cercato fonti accademiche, la regola è quella dell'autore e non serve
altro per metterla in forma. Nessun numero di questa scheda ha una pagina, perché la fonte è
un file di codice.

## Regola eseguibile

Le parti scritte da Mario sono la regola. Dove Mario non dice un dettaglio, la scelta è
marcata **[scelta]** con il perché. Se il codice dell'autore (`OvernightBiasORB.txt`, in
MultiCharts `Mario_OvernightBiasORB`) risolve un dettaglio in modo diverso, vale il codice
dell'autore: è la sua regola, e le mie scelte sono solo la lettura più semplice del testo.

**Mercato e dati.** NQ continuo, barre da 15 minuti costruite dalle barre da 1 minuto,
sessione Globex completa, orari in ora di Chicago (CT). Le barre sono indicate con l'ora di
chiusura, come in MultiCharts: la barra «08:45» va dalle 08:30 alle 08:45. Un contratto
(nella misura: un micro, MNQ, con valori scalati di un decimo).

**Range della notte.** Massimo (ONH) e minimo (ONL) delle barre che chiudono dalle 00:15 alle
08:30 CT dello stesso giorno di calendario. Parte dalla mezzanotte, non dalle 17:00: è la
scelta dell'autore.

**Bias.** Apertura O = open della barra 08:45 (il primo prezzo delle 08:30).
Posizione = (O − ONL) / (ONH − ONL).
- Posizione ≥ 0,67: si possono solo comprare breakout al rialzo.
- Posizione ≤ 0,33: si possono solo vendere breakout al ribasso.
- In mezzo: niente trade quel giorno.
- **[scelta]** Se ONH = ONL, o mancano barre della notte, niente trade: il bias non è definito.

**Opening range.** ORH e ORL = massimo e minimo della barra 08:45. Ampiezza OR = ORH − ORL.
Giorno scartato se l'ampiezza OR di oggi supera 2 volte la EMA a 20 giorni delle ampiezze
OR. **[scelta]** La EMA è calcolata sui 20 giorni precedenti, senza oggi: altrimenti il
giorno anomalo alza la media con cui lo si giudica. Servono 20 giorni di storia prima del
primo trade.

**Setup (si valuta alla chiusura di ogni barra da 15 minuti, con la posizione flat).**
Barre valide per il segnale: quelle che chiudono dalle 09:00 alle 12:00 CT incluse.
Long (solo con bias long), tutte vere alla chiusura della barra:
1. la close supera ORH, e la close della barra precedente era ≤ ORH. **[scelta]** «Prima
   chiusura oltre l'OR» è letta come attraversamento: con fino a 4 trade al giorno, un nuovo
   segnale richiede che il prezzo sia tornato dentro o sotto il livello e lo richiuda sopra.
   Così dopo uno stop non si rientra in automatico alla barra dopo;
2. ADX(16) di Wilder sulle barre da 15 minuti ≥ 20, calcolato in continuo sulla serie Globex;
3. range della barra del segnale (high − low) ≤ 2,5 volte la media semplice dei range delle 20
   barre da 15 minuti precedenti. **[scelta]** «Media di 20» letta come media semplice dei
   range delle 20 barre prima, senza la barra corrente.

Short: speculare (bias short, close sotto ORL con close precedente ≥ ORL, stessi filtri).

**Ingresso.** Ordine a mercato all'apertura della barra successiva al segnale (next bar at
market). L'ultimo ingresso possibile è quindi alle 12:00 CT, sul segnale della barra 12:00.

**Stop.** Distanza S = 0,30 × ATR(15) giornaliero calcolato sulle sole sessioni RTH.
**[scelta]** RTH = 08:30-15:15 CT, le barre giornaliere RTH di NQ; ATR di Wilder sui 15 giorni
precedenti, senza oggi, perché oggi non è finito. Lo stop si misura dalla close della barra
del segnale, come scrive Mario: stop long = close del segnale − S; stop short = close del
segnale + S. Non dal prezzo di ingresso.

**Target.** 3 × S dalla stessa close del segnale: target long = close del segnale + 3S;
target short = close del segnale − 3S. Ordine limite.

**[scelta] Stop e target nella stessa barra.** Il motore lavora a 1 minuto: si guarda quale
livello viene toccato prima nei minuti. Se entrambi sono toccati nello stesso minuto, vale lo
stop (la lettura prudente). Se l'apertura della barra di ingresso è già oltre lo stop o il
target, si esce al prezzo di apertura di quel minuto.

**Uscita a tempo.** Flat alle 14:30 CT, a mercato, su qualunque posizione aperta.

**Massimo di trade.** 4 al giorno, una posizione alla volta. Nessun ingresso mentre c'è una
posizione aperta; un segnale arrivato in quel momento si perde.

**Parametri.** Tutti fissati dall'autore: 67/33%, EMA 20 e 2× per l'OR, ADX(16) ≥ 20, 2,5× la
media di 20 barre, 0,30 × ATR(15), 3R, 08:45-12:00, 14:30, 4 al giorno. Nessuno da
ottimizzare. Il 3R resta 3 anche se il corso, nella Live 006, usa 1,5 (vedi in fondo).

## Frequenza e costi

**Segnali al giorno.** Dai numeri dell'autore: 599 trade in circa 6,7 anni (2020 → agosto
2026), circa 1.680 sessioni, quindi **circa 0,36 trade al giorno**; nel 2006-2019, 1.112 trade
in circa 3.500 sessioni, circa 0,32. Nel nostro 2020-2024 mi aspetto circa 450 trade. Il bias
da solo esclude il terzo centrale dei giorni, e i filtri ne tolgono altri.

**Costi.** L'autore dichiara costi zero. Con $15 andata e ritorno per NQ (il costo che usa
Mario) il lordo dichiarato, circa $430 per trade, è circa 29 volte il costo: per micro circa
$43 contro circa $1,5. Lo slippage dell'ingresso a mercato e dello stop pesa poco rispetto a
uno stop medio di 0,30 ATR giornalieri, che su NQ 2020-2024 vale decine di punti. Sul costo il
problema non c'è: il criterio P6 (lordo ≥ 3 volte il costo) è largamente soddisfatto, se il
lordo dichiarato è vero.

**Dollari al giorno.** Circa $43 per trade × 0,36 trade al giorno ≈ $15 al giorno per micro,
se l'OOS dell'autore si ripete. Sopra il minimo di $10, ma con poco margine.

## Cosa la ucciderebbe, e la soglia della misura

Scritto prima di qualsiasi numero nostro.

**La soglia, sul 2020-2024, al minimo di `perimetro.yaml` e non più bassa:**
- eccesso sul caso / errore standard ≥ **3,0**;
- dollari al giorno per micro, dopo i costi, ≥ **$10**;
- segnali al giorno ≥ **1**.

**Il punto debole, detto ora: la frequenza.** I numeri dell'autore danno circa 0,36 trade al
giorno, un terzo del minimo intraday del perimetro. Se la misura conferma qualcosa di simile,
l'idea muore sulla frequenza anche con un edge vero, e non va salvata allentando i filtri o il
bias: sarebbe un'altra strategia. Con la porta `user` non la cambio, ma secondo me su questo
punto non regge.

**Altre cose che la ucciderebbero:**
- t sotto 3. Per confronto, dai numeri dell'autore (conto mio, non suo): con il 36% di trade
  vinti a 3R, circa 0,43 R per trade, su circa 450 trade, il t del rendimento medio sarebbe
  intorno a 4,5-5. Ma l'eccesso sul caso è più severo del t del rendimento medio, in un
  periodo in cui NQ è salito molto e la regola è spesso long. Se il nostro t sta molto
  sotto 3, l'OOS dell'autore probabilmente è in-sample travestito.
- Il guadagno concentrato in un solo anno (per esempio il 2020) o in pochi giorni: con un
  target a 3R e il 36% di vincite, poche giornate grandi possono fare tutto il risultato.
- Un numero di trade nel 2020-2024 lontano da circa 450 (sotto 300 o sopra 650): vorrebbe
  dire che la nostra lettura della regola non è quella dell'autore, e la misura non giudica
  la sua idea. Va ricontrollata contro il codice prima di decidere.
- Long e short asimmetrici: se tutto il risultato sta nei long, è il rialzo di NQ, non il
  bias della notte.

**Le altre ipotesi nella fonte, una riga ciascuna:**
- La stessa regola con target 1,5R invece di 3R, come gira nel book «Balanced» della Live 006
  del corso (scelta fra 5 uscite su gen 2023 - ago 2025, quindi a posteriori).
