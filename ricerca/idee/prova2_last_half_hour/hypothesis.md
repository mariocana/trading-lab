# prova2_last_half_hour

Porta `user`: l'idea è di Mario (`fonti/idea.md`, aperta il 18/10/2026), qui messa in forma
senza cambiarla. Prova dell'impianto alla cieca: non ho letto il cimitero, quindi non so dire
se è variante di un'idea già morta.

## Ipotesi

Su NQ il rendimento dell'ultima mezz'ora della sessione cash (14:30-15:00 CT) ha lo stesso
segno del rendimento accumulato dalla chiusura cash di ieri fino alle 14:30 di oggi. Comprare
(o vendere) alle 14:30 nella direzione di quel rendimento e uscire alle 15:00 rende più di zero
dopo i costi. È falsa se, sul 2020-2024, il P&L medio per trade dopo i costi non si distingue
da zero alla soglia della sezione 7.

## Meccanismo

Chi è corto gamma sull'indice (i market maker delle opzioni, gli emittenti di ETF a leva e
inversi) per restare coperto deve comprare quando il mercato è salito e vendere quando è
sceso. Gli ETF a leva devono ribilanciare in chiusura per contratto; i dealer di opzioni
concentrano buona parte della copertura verso fine giornata. Il flusso va quindi nella
direzione del movimento della giornata e arriva negli ultimi minuti: spinge il prezzo
dell'ultima mezz'ora nello stesso verso. È un flusso obbligato, non una scelta: il dealer non
decide se coprirsi, l'ETF a leva non decide se ribilanciare.

Secondo Mario il paper lo controlla direttamente: l'effetto è più forte quando l'esposizione
gamma netta dei dealer (proxy dalle opzioni S&P 500) è più negativa. Sempre secondo la sintesi
del paper, la spinta si riassorbe nei giorni successivi, come ci si aspetta da una pressione
di liquidità e non da un'informazione.

## Chi perde, e perché continua a perdere

Chi paga è chi deve coprirsi: i dealer corti gamma e gli emittenti di ETF a leva. Comprano
dopo i rialzi e vendono dopo i ribassi, a prezzi spinti dal loro stesso flusso. Non smettono
perché coprirsi è un obbligo di rischio (per i dealer) o contrattuale (per gli ETF a leva). Il
costo lo passano a valle: ai compratori di opzioni nel premio, ai detentori di ETF a leva nel
rendimento peggiore dell'indice moltiplicato per la leva. Chi vende loro liquidità nell'ultima
mezz'ora, cioè chi va contro il movimento della giornata, incassa quel costo; la strategia
prova a stare dalla parte opposta, cioè davanti al flusso.

Punto aperto: dal 2022 le opzioni 0DTE hanno cambiato il posizionamento gamma dei dealer, e
non so dire in che verso. Se oggi i dealer sono lunghi gamma in netto nel pomeriggio, il flusso
si inverte e il chi perde sparisce. Mario lo dichiara nella sua scheda.

## Fonti

Tipo di fonte: **paper**.

**Baltussen, G., Da, Z., Lammers, S., Martens, M. (2021), «Hedging demand and market intraday
momentum», Journal of Financial Economics 142(1), pp. 377-403**, DOI 10.1016/j.jfineco.2021.04.029
(working paper: SSRN 3760365).

Cosa ho verificato: i dati bibliografici (rivista, volume, pagine, DOI) e il contenuto
dell'abstract da indici pubblici (RePEc/EconPapers, Erasmus repository): oltre 60 futures su
azioni, obbligazioni, materie prime e valute, 1974-2020; il rendimento degli ultimi 30 minuti
prima della chiusura è previsto in positivo dal rendimento del resto della giornata; la
previsione si inverte nei giorni successivi; il legame con la copertura corta gamma di dealer
di opzioni e di ETF a leva. Non ho visto la pagina dell'abstract (di regola p. 377), quindi
anche questo è senza pagina controllata.

Cosa **non** ho verificato: il PDF dell'autore (nd.edu/~zda/intramom.pdf) l'ho scaricato ma non
sono riuscito ad aprirlo come testo. Nessuno dei numeri e delle pagine che seguono è stato
controllato da me sulla pagina; li riporto come li ha scritti Mario, con il suo rimando:

| cosa dice, secondo Mario | dove, secondo Mario | stato |
|---|---|---|
| regressione per mercato del rendimento dell'ultima mezz'ora su r_ROD: NQ t 7,97, R² 4,10%, R² fuori campione 3,76%, 1996-2020; ES t 4,97; RTY t 5,86; YM t 4,12 | Tab. B1 | non verificato |
| r_ROD va dalla chiusura di ieri a 30 minuti dalla chiusura di oggi, notte compresa | definizione del paper | non verificato |
| la strategia: posizione nella mezz'ora finale con il segno di r_ROD | eq. 12 | non verificato |
| portafoglio equipesato dei futures azionari, senza costi: 6,86% annuo, Sharpe 1,73, 55% dei giorni in utile; con il filtro «entrambi i segnali concordi» 61% e Sharpe 1,60 | non indicata | non verificato, senza pagina |
| «we do not consider transaction costs»; su ES lo Sharpe resta positivo con un costo di un tick | p. 386 | non verificato |
| risultati simili nei sottoperiodi 1974-1999 e 2000-2020 | §3.4, Tab. 5 | non verificato |
| l'effetto cresce quando la gamma netta è più negativa | §4 | non verificato |

Il critico deve trattare la tabella come affermazioni da controllare, non come fonti con
pagina. L'unico numero di cui rispondo è il riferimento bibliografico.

## Regola eseguibile

| | |
|---|---|
| mercato | NQ, contratto continuo, 1 contratto (la misura scala per i micro) |
| timeframe | barre da 5 minuti, ora di Chicago. Ogni barra porta l'orario della sua chiusura: la barra «14:30» copre 14:25-14:30 |
| setup | ogni sessione in cui esistono sia la barra delle 14:30 di oggi sia la barra delle 15:00 di oggi |
| segnale | `r_ROD = Close(14:30 di oggi) / Close(15:00 dell'ultima sessione precedente che ha una barra delle 15:00) - 1`. Notte compresa, come nella definizione di Mario |
| direzione | LONG se r_ROD > 0, SHORT se r_ROD ≤ 0 (Mario: «SHORT altrimenti»; r_ROD = 0 esatto va short, è la lettura letterale) |
| ingresso | a mercato, al prezzo di chiusura della barra delle 14:30 (scelta: è il prezzo su cui si calcola il segnale; se il motore entra solo all'apertura della barra successiva, apertura della barra 14:30-14:35, che è lo stesso istante) |
| stop | nessuno (Mario: la strategia del paper non ne ha) |
| target | nessuno |
| uscita a tempo | a mercato, al prezzo di chiusura della barra delle 15:00 CT |
| finestra oraria | solo 14:30-15:00 CT; niente altro nella giornata |
| massimo trade al giorno | 1 |
| giorni esclusi | sessioni a chiusura anticipata e ogni sessione in cui manca la barra delle 14:30 o quella delle 15:00: nessun trade (Mario). Il riferimento di ieri salta i giorni senza barra delle 15:00 (scelta mia: la lettura più semplice di «chiusura di ieri») |
| ora legale | nessuna correzione: le 14:30 e le 15:00 sono sempre ora di Chicago, che segue la chiusura cash |
| flat a fine giornata | sì, alle 15:00 CT, prima della chiusura di Globex |
| costi | $7,50 per lato per contratto NQ, cioè $15 andata e ritorno = 0,75 punti (convenzione di Mario) |
| parametri liberi | nessuno. Il filtro «entrambi i segnali concordi» non si testa (Mario) |

## Frequenza e costi

**Segnali al giorno:** uno per sessione, tutti i giorni tranne le chiusure anticipate (circa
3-4 l'anno). Sul 2020-2024 sono circa 1.250 trade. Attenzione al minimo del perimetro
(`segnali_al_giorno_min: 1`): contata su tutte le sessioni la frequenza è circa 0,99, appena
sotto 1; contata sulle sessioni in cui la regola è attiva è 1. Il desk decida quale conteggio
vale, prima della misura.

**Effetto contro costo.** Il paper, per quel che riporta Mario, non mette i costi, salvo una
frase su ES con un tick. Faccio un conto mio, da prendere come ordine di grandezza perché parte
da un numero non verificato: 6,86% annuo su circa 252 giorni è circa 2,7 punti base al giorno.
Su NQ intorno a 13.000 punti (livello tipico del 2020-2024) sono circa 3,5 punti a trade lordi,
contro 0,75 punti di costo: l'effetto lordo è circa quattro-cinque volte il costo. Ma la soglia
del perimetro è in dollari: $10 al giorno per micro sono 5 punti netti al giorno su MNQ ($2 a
punto). Con un trade al giorno servono quindi circa 5,75 punti lordi medi a trade. Il numero del
paper (portafoglio di quattro indici, prima del decadimento) ne promette circa 3,5. NQ è più
volatile della media del portafoglio e potrebbe dare di più in punti, ma sulla carta l'idea
arriva alla soglia in dollari solo se su NQ l'effetto è circa una volta e mezza quello medio del
paper, e senza decadimento.

## Cosa la ucciderebbe, e la soglia della misura

Scritto prima di qualsiasi numero.

**Soglia della misura (2020-2024, in-sample):** eccesso / errore standard ≥ **3,0** e almeno
**$10 al giorno per micro** dopo i costi. Sono i minimi del perimetro; non li alzo. La soglia di
Mario (Gate 2, t ≥ 2) è sotto il minimo del perimetro e qui non vale: vale 3,0.

Con il conto di Mario (t atteso 3,64 a effetto intatto, 1,82 a effetto dimezzato), t ≥ 3,0
passa solo se sopravvive circa l'82% dell'effetto. La sua stessa aspettativa dichiarata è
«effetto dimezzato», cioè sotto soglia. Lo scrivo perché con la porta `user` non tocca a me
cambiare l'idea, ma la previsione di Mario è che non passi.

**La uccide:**
1. eccesso / errore standard sotto 3,0 sul 2020-2024;
2. meno di $10 al giorno per micro dopo $15 andata e ritorno per contratto, anche con t ≥ 3
   (secondo il conto della sezione 6 è il rischio più probabile);
3. quota di trade in utile vicina al 50% (Mario guarda il segno), oppure segno sopra il 50% ma
   mossa media dei perdenti grande quanto quella dei vincenti, cioè guadagno atteso nullo;
4. un risultato che regge solo in un anno (per esempio il 2020, ancora dentro il campione del
   paper fino a maggio) e sparisce nel 2022-2024, quando sono cresciute le 0DTE: lo direi
   decaduto, non vivo.

**Due punti deboli che segnalo al critico.**
- Il t di Mario viene dalla regressione del paper riscalata sulla radice del numero di giorni.
  Non è la stessa statistica dell'eccesso per trade che misura il motore: la stima 3,64 è
  indicativa, non una previsione della misura.
- Nessuna pagina è stata verificata da me (sezione 4). Se il critico apre il paper e la
  definizione di r_ROD non comprende la notte, o la chiusura di riferimento non è quella cash
  delle 15:00 CT, la regola va riallineata alla fonte prima della misura.

**Altre ipotesi nella stessa fonte** (non aperte, decide il desk):
- il filtro «entrambi i segnali concordi» (prima mezz'ora e r_ROD dello stesso segno): meno
  trade, 61% di successo secondo Mario;
- la stessa regola condizionata alla gamma netta dei dealer (serve un dato che non abbiamo);
- l'inversione nei giorni successivi (orizzonte daily, spento nel perimetro).
