# hyperliquid-bridge

Il connettore verso Hyperliquid: esecuzione, rischio e journal. **Non contiene strategie e
non decide niente.** Il segnale nasce in MultiCharts; questo pacchetto servirà a copiare su un
perp la posizione che MultiCharts vuole, come fa il bridge MT5 sui CFD.

**Stato (17/11/2026): il follower c'è e gira su un conto paper a prezzi veri; non è mai stato
provato su Hyperliquid con ordini.** `hlbridge follow` legge i file di stato di MultiCharts e copia la
posizione. Prima di un ordine vero mancano lo stop sull'exchange e la prova su testnet, in fondo.

Fino al 12/11/2026 era `trading-desk`, un desk autonomo con una strategia sua (`reversal_v1`,
bocciata in validation). Strategie, ciclo giornaliero, shadow mode e time stop sono stati
tolti: restano in git fino al commit `74ae180`.

## Cosa c'è

| modulo | cosa fa |
|---|---|
| `hlbridge/execution/hyperliquid.py` | ordini con un API wallet che non può prelevare; idempotenza per `cloid`; riconciliazione dei fill |
| `hlbridge/execution/ledger.py` | quale posizione è nostra, chi l'ha aperta e quando; una posizione non nostra non si tocca |
| `hlbridge/execution/paper.py` | conto simulato ai prezzi veri, con i costi misurati (maker 1,5 bps, taker 4,5 + 7,3 bps) |
| `hlbridge/risk/` | il motore di rischio (limiti in `config/limits.yaml`), lo stato (perdita del giorno, drawdown, halt) e il kill switch |
| `hlbridge/data/hl_market.py` | prezzi, funding, book e stato del conto, in sola lettura |
| `hlbridge/data/market_record.py` | ogni ora lo stato grezzo del mercato in `var/market/`, per quantlake: open interest e listini non si riscaricano |
| `hlbridge/journal/`, `hlbridge/pm/` | journal append-only e avvisi Telegram |
| `hlbridge/ui/` | pagina di controllo: conto, posizioni, limiti, kill switch, chiusura di tutto |
| `hlbridge/follow/` | **il bridge**: legge `mario_stato_<STRAT>.csv`, agisce solo sui cambi di posizione, apre con lo stop d'emergenza dal file, chiude il lato sbagliato prima di aprire, passa dal motore di rischio, guarda perdita del giorno e drawdown ogni minuto |
| `config/bridge.yaml` | quali strategie seguire, su quale perp, quanti micro valgono, che scala, limiti del bridge |

## Il bridge

```text
strategia sul grafico → Mario_BridgeStato → mario_stato_<STRAT>.csv → hlbridge follow → perp su Hyperliquid
```

Il file è quello del bridge a stato di `multicharts/bridge/SPEC.md` (una riga, `DPB;NQ;-1;120.00;FINE`).
Le regole sono quelle dell'EA di MT5: agisce solo sui cambi, non riapre se lo stop chiude e MultiCharts
non cambia, all'avvio non insegue niente (se MultiCharts e Hyperliquid sono diversi lo dice), un cambio
di size dentro un trade non si copia, cinque tentativi per cambio e poi si ferma e avvisa.

**Gira sul VPS di MultiCharts**, accanto al file. Non su Railway: lì resta solo la pagina di controllo.

```bash
HL_DEXS=xyz .venv/bin/hlbridge follow            # conto paper, prezzi veri
HL_DEXS=xyz .venv/bin/hlbridge follow --live     # ordini veri (testnet salvo HL_TESTNET=0)
```

- **Strumenti.** NQ → `xyz:XYZ100`, il perp del dex HIP-3 `xyz` che segue il Nasdaq-100 (circa $680 milioni
  al giorno sul mainnet). 1 MNQ vale $2 per punto e 1 unità del perp $1 per punto: `unita_per_micro: 2`.
  **Da riverificare sulle specifiche del contratto.** Il testnet lista solo `XYZ100`, con volume nullo; ES
  (`xyz:SP500`) e GC (`xyz:GOLD`) non sono ancora in `bridge.yaml`.
- **Scala.** `scala: 0.05` copia il 5% della size di MultiCharts: su un demo piccolo non si parte a uno a uno.
- **Una strategia per perp.** Hyperliquid tiene una posizione netta per perp: DPB e OBO sono entrambe su NQ e la
  config rifiuta di seguirle insieme. Serve un subaccount per strategia.
- **Stop.** Dal file, in punti, dal prezzo medio al momento dell'ordine. Se dopo l'apertura il ledger non ha lo
  stop, il bridge avvisa e non fa altro (vedi sotto).
- **Chiusura.** `market_close` della posizione intera, poi cancella gli ordini rimasti per quel perp, stop
  compreso: uno stop vecchio non deve proteggere la posizione dopo.
- **HIP-3.** Le posizioni e il margine di un dex sono separati da quelli del dex principale: `HLMarket` e
  l'adapter ora li leggono (`HL_DEXS=xyz`). Il client riceve `perp_dexs=['', 'xyz']`: l'SDK carica **solo** i
  dex elencati, quindi senza `''` BTC e gli altri non si risolverebbero. Controllato contro l'SDK, non
  contro un ordine: `xyz:XYZ100` ha asset id 110000 sul mainnet e 750000 sul testnet.
- **Il prezzo viene dal posto dove riposa l'ordine.** Sul testnet `XYZ100` sta a 30.613 e sul mainnet a 26.995
  (13% di differenza): con il prezzo del mainnet lo stop di uno short finiva sotto il mercato e scattava
  subito. Con `--live` la size in dollari e lo stop usano il book di esecuzione; i limiti di liquidità
  (volume, profondità) restano quelli del mainnet, perché il testnet non ha volume.

## La prova su testnet del 17/11

Con la chiave API wallet, su `xyz:XYZ100`, conto unificato:

| | esito |
|---|---|
| Firma dell'API wallet e asset id 750000 del perp HIP-3 | **ok**: l'exchange arriva a validare l'ordine |
| Margine di un perp HIP-3 su un conto unificato (il dex `xyz` ha saldo 0) | **ok**: un ordine a riposo di $20 è accettato |
| Ordine, elenco degli ordini per dex, `cancel_asset_orders` | **ok**: l'ordine compare nell'elenco di `xyz` e si cancella |
| Il follower che apre, con lo stop, e chiude, su `xyz:XYZ100` | **non provato**: nessun ordine IOC si è riempito |
| Lo stesso percorso su `BTC` del testnet (un perp normale, book largo 12 bps) | **ok**: short di 0,0004 BTC (~$25) riempito, stop-market di $300 piazzato sull'exchange e presente nel ledger, flat che chiude con `market_close` e cancella lo stop; le altre 9 posizioni del conto restano com'erano |

Perché nessun fill: il book del testnet è bid 28.226 / ask 33.000 contro un mark di 29.368 e un oracolo
di 28.180, e l'exchange rifiuta (`Price too far from oracle`) ogni prezzo a cui questo book si può
attraversare. Un ordine a 29.074 (1% sotto il mark) passa, uno a 28.225 (3,9% sotto) no: la banda sembra
centrata sul **mark**, non sul prezzo medio del book. Per aprire una posizione di prova serve un
book con liquidità dentro la banda: il mainnet (XYZ100 fa circa $680 milioni al giorno) o un altro perp
del testnet. Quindi **su un perp HIP-3 restano non provati** il fill, lo stop e `market_close`; sul dex
principale il percorso intero è provato (riga di `BTC`).

Trovato lungo la strada: `book_depth_10bps` non risolveva i nomi HIP-3 (`KeyError`), e senza il prezzo
di esecuzione il follower ordinava al prezzo del mainnet; ora non ordina se non vede il book.

## Cosa manca prima di un ordine vero

1. **Lo stop d'emergenza sull'exchange** (dall'audit del 12/11). Oggi `_place_stop` parte solo se l'ordine è
   eseguito subito; il follower usa ordini IOC, che si eseguono subito, ma se il fill è parziale o l'ordine
   non entra lo stop non c'è. Sul testnet 44 posizioni su 44 erano rimaste senza stop con gli ordini post-only.
2. **La prova su testnet con `xyz:XYZ100`.** Cosa verificare: firma e asset id di un perp HIP-3, la lettura delle
   posizioni per dex, `cancel_asset_orders` (elenco ordini per dex), `market_close`, che il margine del dex
   sia finanziato, e che 0,1 unità superi il minimo d'ordine.
3. **Limiti per strategia.** C'è la sezione `limiti` di `bridge.yaml`, vuota: il 2% dell'equity per un perp
   HIP-3 di `limits.yaml` taglia una posizione sola, e il follower avvisa quando taglia. Il numero giusto lo
   scegli tu.
4. **Un subaccount per strategia**, e un allarme quando il bridge non riesce a seguire MultiCharts (oggi avvisa
   dopo i tentativi falliti, non se il file smette di aggiornarsi).
5. **`watch_risk` chiude tutto il conto.** Se la perdita del giorno supera il limite chiama `flatten_all`, che
   chiude anche posizioni che non sono del bridge e cancella tutti gli ordini. Prima di questo commit nessuno
   consumava quel flag. Se debba chiudere tutto o solo i perp del bridge lo decidi tu.
6. **Nessun avviso se il file non si legge mai.** Con la cartella sbagliata o una codifica diversa il bridge
   sembra vivo e non fa niente: serve un avviso quando un file non si aggiorna o non esiste da troppo.
7. **Windows.** Il comando di `follow` sul VPS non è mai stato lanciato lì: i percorsi qui sopra sono quelli
   di macOS (`.venv/Scripts/` su Windows).
8. **Il file in tempo reale.** Mai provato: `Mario_BridgeStato` e l'EA di MT5 sono mai stati compilati (vedi la
   SPEC del bridge). Il follower è provato solo con file scritti a mano.

## Uso

```bash
uv venv --python 3.12 .venv && uv pip install -p .venv/bin/python -e ".[dev]"
.venv/bin/python -m pytest -q
.venv/bin/hlbridge status          # conto paper, prezzi veri
.venv/bin/hlbridge ui              # pagina di controllo su 127.0.0.1:8765
.venv/bin/hlbridge kill            # kill switch: nessun rischio nuovo, chiudere resta permesso
```

`.env` da `.env.example`. La chiave è quella dell'API wallet, mai quella del conto. `HL_TESTNET=1`
è il default. Le variabili della pagina hanno ancora il prefisso `DESK_` (`DESK_PASSWORD`,
`DESK_MODE`, `DESK_SNAPSHOT_MINUTES`, `DESK_MARKET_MINUTES`): non le ho rinominate per non
rompere la configurazione che c'è su Railway.

`scripts/testnet_smoke.py` manda un ordine solo su testnet e lo chiude: prova che firma,
ordine, fill e riconciliazione funzionano. `scripts/spot_to_perps.py` sposta USDC da spot a
perp su testnet.

## Deploy

Su Railway il servizio era configurato sulla cartella `trading-desk/`. **Con questo nome nuovo
vanno cambiati a mano, nelle impostazioni del servizio, Root Directory e Watch Paths**
(`hyperliquid-bridge` e `hyperliquid-bridge/**`); il comando d'avvio è `hlbridge ui`
(`railway.json`). Finché non si cambia, il deploy dal ramo con la cartella rinominata fallisce.
`var/` va su un volume: tiene journal, stato del rischio e registro del mercato.
