"""La meccanica di una strategia sull'in-sample, senza un solo numero di performance.

    PYTHONPATH=multicharts python3 -m motore.meccanica monday_long
    PYTHONPATH=multicharts python3 -m motore.meccanica monday_long --giorno 2020-03-16
    PYTHONPATH=multicharts python3 -m motore.meccanica dpb DriftMode=1

Serve a chi scrive la strategia per controllare che i trade stiano dove la regola dice: quanti
sono, in che giorni e a che ora si entra e si esce, quanti al giorno, quanti a cavallo di due
date. E' il controllo che il coder del desk di ricerca puo' fare, perche' qui non esce niente
che dica se la regola guadagna.

Cosa NON stampa, e non va aggiunto: prezzi, punti, dollari, escursioni, e quante uscite ha ogni
segnale. Contare le uscite a target contro quelle a stop e' un win rate. Per lo stesso motivo
delle uscite si danno solo il primo e l'ultimo orario, non la distribuzione, e della durata solo
la piu' corta e la piu' lunga.
"""
import argparse, collections, datetime as dt

GIORNI = ('lun', 'mar', 'mer', 'gio', 'ven', 'sab', 'dom')


def _ora(t):
    return t.strftime('%H:%M')


def meccanica(trade, giorni_di_mercato):
    """trade: i Trade del motore. Ritorna solo conteggi, giorni e orari."""
    n = len(trade)
    m = {'trade': n, 'giorni_di_mercato': giorni_di_mercato}
    if not n:
        return m
    per_giorno = collections.Counter(t.t_in.date() for t in trade)
    durate = [t.t_out - t.t_in for t in trade]
    m.update(
        per_anno=dict(sorted(collections.Counter(t.t_in.year for t in trade).items())),
        giorni_con_trade=len(per_giorno),
        massimo_in_un_giorno=max(per_giorno.values()),
        long=sum(t.lato > 0 for t in trade),
        short=sum(t.lato < 0 for t in trade),
        ingressi_per_giorno_della_settimana={GIORNI[k]: v for k, v in sorted(
            collections.Counter(t.t_in.weekday() for t in trade).items())},
        ingresso_primo=_ora(min(t.t_in.time() for t in trade)),
        ingresso_ultimo=_ora(max(t.t_in.time() for t in trade)),
        ingressi_orari_piu_frequenti=[[_ora(k), v] for k, v in collections.Counter(
            t.t_in.time() for t in trade).most_common(5)],
        uscite_giorni_della_settimana=[GIORNI[k] for k in sorted({t.t_out.weekday() for t in trade})],
        uscita_prima=_ora(min(t.t_out.time() for t in trade)),
        uscita_ultima=_ora(max(t.t_out.time() for t in trade)),
        a_cavallo_di_due_date=sum(t.t_in.date() != t.t_out.date() for t in trade),
        durata_piu_corta=str(min(durate)),
        durata_piu_lunga=str(max(durate)),
        segnali_di_ingresso=sorted({t.nome_in for t in trade}),
        segnali_di_uscita=sorted({t.nome_out for t in trade}),      # i nomi, mai i conteggi
    )
    return m


def del_giorno(trade, giorno):
    """I trade entrati o usciti quel giorno: solo segnale d'ingresso e orari."""
    return [(t.nome_in, 'long' if t.lato > 0 else 'short', str(t.t_in), str(t.t_out))
            for t in trade if giorno in (t.t_in.date(), t.t_out.date())]


def stampa(m):
    print('  trade                    %d' % m['trade'])
    if not m['trade']:
        print('  nessun trade: la regola non scatta mai, o c\'e\' un bug')
        return
    print('  per anno                 ' + ' · '.join('%d: %d' % kv for kv in m['per_anno'].items()))
    print('  giorni con un ingresso   %d su %d di mercato · massimo in un giorno %d' % (
        m['giorni_con_trade'], m['giorni_di_mercato'], m['massimo_in_un_giorno']))
    print('  lato                     long %d · short %d' % (m['long'], m['short']))
    print('  ingressi, giorno         ' + ' · '.join('%s %d' % kv for kv in m['ingressi_per_giorno_della_settimana'].items()))
    print('  ingressi, orario         dalle %s alle %s · i piu\' frequenti: %s' % (
        m['ingresso_primo'], m['ingresso_ultimo'],
        ', '.join('%s (%d)' % tuple(x) for x in m['ingressi_orari_piu_frequenti'])))
    print('  uscite, giorno           ' + ' · '.join(m['uscite_giorni_della_settimana']))
    print('  uscite, orario           dalle %s alle %s' % (m['uscita_prima'], m['uscita_ultima']))
    print('  a cavallo di due date    %d' % m['a_cavallo_di_due_date'])
    print('  durata                   la piu\' corta %s · la piu\' lunga %s' % (m['durata_piu_corta'], m['durata_piu_lunga']))
    print('  segnali                  ingresso: %s · uscita: %s' % (
        ', '.join(m['segnali_di_ingresso']), ', '.join(m['segnali_di_uscita'])))


def main():
    from . import dati, esegui
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('nome', help='la strategia nel registro del motore (motore/strategie/__init__.py)')
    ap.add_argument('input', nargs='*', help='input della strategia, chiave=valore')
    ap.add_argument('--giorno', type=dt.date.fromisoformat,
                    help='elenca i trade entrati o usciti quel giorno (AAAA-MM-GG): segnale e orari')
    a = ap.parse_args()
    inp = {k: esegui.valore(v) for k, v in (x.split('=', 1) for x in a.input)}
    dal, al = esegui.IS
    trade, _, reg = esegui.gira(a.nome, dal, al, inp)
    if a.giorno:
        righe = del_giorno(trade, a.giorno)
        print('%s, %s: %d trade' % (a.nome, a.giorno, len(righe)))
        for r in righe:
            print('  %s %s  %s -> %s' % r)
        return
    giorni = {b.t.date() for b in dati.barre(reg['simbolo'], reg['tf'][0], dal, al) if b.t.weekday() < 5}
    print('%s su %s, %s -> %s (solo meccanica)' % (a.nome, reg['simbolo'], dal, al))
    stampa(meccanica(trade, len(giorni)))


if __name__ == '__main__':
    main()
