# Critica — prova2_orb_breakout

**1. Tipo di fonte:** `praticante` (un corso, citato senza nome, autore né data; il materiale non è in `fonti/`).

**2. Filtro dei praticanti**

| voce | esito | perché |
|---|---|---|
| P1 regole complete | sì | range, setup, ingresso, stop, target, uscita a tempo e massimo trade fissati; le scelte di esecuzione sono dichiarate, nessun parametro libero |
| P2 dati oltre il 2021 | non verificato | «NQ 2021-26» lo riferisce Mario; il corso non si apre |
| P3 OOS dichiarato e separato | non verificato | il corso, per quanto riportato, non lo dice; la «live indipendente» non ha nome |
| P4 flat entro la sessione | sì | uscita a tempo alle 14:00 CT, o sull'ultima barra nelle sessioni corte |
| P5 stop dichiarato | sì | stop fisso al minimo del range |
| P6 costi o edge ≥ 3× costo | non verificato | costi non dichiarati; sul numero riferito (~9 pt contro ~1 pt di costo) passerebbe, ma il numero non è verificabile |
| testata sui nostri futures | non verificato | dichiarata su NQ, senza materiale |
| track record live | no | nessuno dichiarato |
| trade nell'OOS | non verificato | non dichiarati |
| parametri ottimizzati | non verificato | non dichiarati; il «cluster a 30-32 minuti» viene da una fonte senza nome |
| chi perde | non verificato | «chi fa fade dell'apertura», senza fonte; l'autore lo dà come non stabilito |

**3. Il conto** (MNQ: 1 pt = $2; costo andata e ritorno per micro ~ $2, commissione più un tick per lato)

- *Favorevole*: 1 trade/giorno, il massimo della regola. Edge $183/NQ, cioè $18,3/micro, preso come lordo: (18,3 − 2) × 1 = **$16,3/giorno**, sopra i $10. Se i $183 sono già netti: $18,3.
- *Alla frequenza dichiarata* (~0,6/giorno, 823 trade su ~1.350 sessioni): 0,6 × 16,3 = **$9,8/giorno** se lordo, sotto il minimo; 0,6 × 18,3 = $11 se netto.
- *Prudente*: 0,6/giorno, edge dimezzato (fonte di venditore, nessun OOS): 0,6 × (9,15 − 2) = **$4,3/giorno**, sotto. Con il netto della fonte 3 (≈ 0 R, su un'altra regola della famiglia) si va a ~$0.
- Coerenza interna: WR 58% con bracket 1R fa ~0,16 R lordi; con $183 vuol dire R ≈ 57 pt, plausibile per un range di 30 minuti su NQ nel 2021-24.

Passa nel caso favorevole, non in quello prudente: è un punto debole, non un KILL.

**4. Punti deboli**

1. **Fonte principale non verificabile.** I numeri del corso (823 trade, WR 58%, $183, PF 1,28) arrivano solo dalle note di Mario: niente costi, niente OOS e niente conteggio dei parametri dichiarati. P2, P3 e P6 restano non verificati.
2. **La fonte indipendente più vicina va contro.** La replica di Krueger (fonte 3, su un'altra regola della famiglia: range di 5 minuti, 10R) trova su NQ un lordo pari al costo e un netto di 0,0 R (t 0,0), con al più +0,06 R nel 2021-26. Il range di 30 minuti diluisce il costo in R, ma è un argomento, non una misura.
3. **Frequenza al limite.** Il massimo è 1 al giorno, quindi la regola non è fuori perimetro. La media attesa di ~0,6 sta però sotto `segnali_al_giorno_min` e anche il conto a frequenza dichiarata è sotto i $10 se i $183 sono lordi.
4. **Nessun flusso obbligato e nessun perdente stabilito.** È un pattern di continuazione: gli ordini a benchmark di sessione non sono vincolati alla direzione della rottura. Il fade dell'apertura è un racconto senza fonte.
5. **Deriva e sovrapposizione del campione.** È solo long su NQ 2020-24, in forte rialzo: senza un caso nullo solo-long con lo stesso bracket, l'eccesso è gonfiato. Inoltre il nostro in-sample copre il periodo mostrato dal corso (2021-24), quindi una misura positiva conferma il backtest del venditore e non lo mette alla prova fuori campione.

RISERVA: sì (P2, P3 e P6 non verificati, e la replica indipendente più vicina dice che il netto è zero)

VERDETTO: GO
