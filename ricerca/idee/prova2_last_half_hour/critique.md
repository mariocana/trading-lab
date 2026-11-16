# Critica: prova2_last_half_hour

**Tipo di fonte:** `paper` (Baltussen, Da, Lammers, Martens, JFE 142(1), 2021, pp. 377-403).

Cosa ho aperto: la scheda EconPapers conferma rivista, volume, pagine, DOI e l'abstract:
più di 60 futures dal 1974 al 2020, ultima mezz'ora prevista dal resto della giornata,
inversione nei giorni dopo, legame con la copertura corta gamma di market maker ed ETF a leva.
Il PDF dell'autore si scarica ma non riesco a estrarne il testo; SSRN risponde 403. **Nessuna
pagina interna è verificata**: Tab. B1, eq. 12, p. 386, §3.4, §4 e la definizione di r_ROD
restano affermazioni di Mario.

## Filtro

| # | voce | esito | perché |
|---|---|---|---|
| 1 | testato su futures | sì | l'abstract dice futures; i numeri su NQ (Tab. B1) non sono verificati |
| 2 | replicato | sì | più di 60 mercati e 46 anni secondo l'abstract; la replica indipendente non è verificata |
| 3 | flusso obbligato | sì | l'abstract lo lega alla copertura gamma; il test condizionato (§4) non è verificato |
| 4 | costi riportati, edge > costo | non verificato | secondo Mario i costi non sono modellati (p. 386 non aperta) |
| 5 | intraday, flat in sessione | sì | un trade 14:30-15:00 CT, flat alla chiusura cash |
| 6 | età | no | dati fino al 2020, pubblicato nel 2021: più di 4 anni, aspettarsi metà edge |
| 7 | t ≥ 3 | non verificato | t 7,97 su NQ secondo Mario, tabella non aperta |
| 8 | campione oltre il 2021 o conferma recente | no | l'abstract dice che il campione finisce nel 2020; nessuna conferma recente citata |
| 9 | dati accessibili | sì | la regola base usa solo prezzi NQ; la variante con gamma (dato che non abbiamo) non è la regola |

## Il conto

Soglia: $10 al giorno per micro = 5 punti MNQ netti al giorno. Costo 0,75 punti a trade.
Frequenza massima: 1 trade al giorno, quindi servono **5,75 punti lordi medi a trade**.

- **Caso favorevole** (1 al giorno, l'edge di NQ dichiarato da Mario). Dall'R² di 4,10% su NQ
  la correlazione è circa 0,20. Per una regola che usa solo il segno, l'edge è circa
  0,20 × 0,8 × σ dell'ultima mezz'ora. Stimo io σ a circa 0,4% (circa 50 punti a 13.000):
  stima mia, non della fonte. Vengono **circa 8,5 punti lordi**, 7,8 netti, **circa $15,5 al
  giorno per micro**. Passa. Con lo Sharpe del portafoglio (1,73, cioè 0,11 al giorno ×
  50 punti) vengono circa 5,8 punti lordi: sta proprio al minimo.
- **Caso prudente** (il 6,86% annuo del portafoglio preso alla lettera, circa 3,5 punti a 13.000,
  dimezzato dopo la pubblicazione). Restano 1,75 punti lordi e 1,0 netto, **circa $2 al giorno
  per micro**. Non passa.

Passa solo nel caso favorevole. È un punto debole, non un KILL.

## Punti deboli

1. **Il campione finisce nel 2020 (voce 8: no).** Il 2020-2024 è quasi tutto dopo la
   pubblicazione e dopo l'esplosione delle 0DTE. Se nel pomeriggio i dealer sono lunghi gamma
   in netto, il flusso cambia verso e il perdente sparisce: lo dice l'ipotesi stessa.
2. **Nessuna pagina interna è verificata.** Il t su NQ, l'R², la definizione di r_ROD (notte
   compresa? quale chiusura di riferimento per i futures?) e la frase sui costi sono di seconda
   mano. Se r_ROD non è definito così, la regola misura un'altra cosa.
3. **Il conto in dollari è stretto.** Servono 5,75 punti lordi a trade. Passa solo con l'edge
   specifico di NQ intatto. Con l'edge medio dimezzato resta a circa un quinto della soglia.
4. **La significatività attesa è sotto 3 con l'edge dimezzato.** Il conto di Mario dà t 3,64 con
   l'edge intatto e 1,82 con l'edge dimezzato, e Mario stesso si aspetta un edge dimezzato.
   Quel t viene da una regressione, non dall'eccesso per trade.
5. **Nessuno stop e un solo trade al giorno.** Il P&L dipende da poche giornate di grande
   escursione nell'ultima mezz'ora (2020, 2022): il risultato può reggersi su un anno solo.

Nota di processo: cercando le voci 8 e 9 del filtro con una ricerca mirata, ho letto la riga 112
di `come_scegliere_un_paper.md`, che riporta un esito su questa idea. Il verdetto sotto non ne
tiene conto: la voce 8 è `no` già per l'abstract (campione al 2020) e le ragioni di KILL non
dipendono da misure.

RISERVA: sì (manca la voce eliminatoria 8: campione fermo al 2020, nessuna conferma recente)

VERDETTO: GO
