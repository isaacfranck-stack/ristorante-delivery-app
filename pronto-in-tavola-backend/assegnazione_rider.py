"""
assegnazione_rider.py - Logica di assegnazione automatica del rider

Questo modulo implementa l'algoritmo descritto nel documento di progetto:
    punteggio = distanza + (numeroOrdiniAttivi * 2)
Il rider con punteggio più basso vince: è il più vicino e meno carico.

Le zone usate nel progetto sono semplici stringhe ("centro", "nord", "sud", "est", "ovest").
La distanza viene calcolata con una tabella fissa (nessuna API esterna necessaria).
"""

from database import db, Rider, Ordine

# ─────────────────────────────────────────────
#  TABELLA DELLE DISTANZE TRA ZONE
# ─────────────────────────────────────────────

# Le zone della città in cui il ristorante opera.
# La distanza è un numero intero: 1 = stessa zona, 2 = vicina, 3 = lontana.
# La tabella è simmetrica: distanza(A, B) == distanza(B, A)

DISTANZE = {
    ("centro", "centro"): 1,
    ("centro", "nord"):   2,
    ("centro", "sud"):    2,
    ("centro", "est"):    2,
    ("centro", "ovest"):  2,
    ("nord",   "nord"):   1,
    ("nord",   "sud"):    3,
    ("nord",   "est"):    2,
    ("nord",   "ovest"):  2,
    ("sud",    "sud"):    1,
    ("sud",    "est"):    2,
    ("sud",    "ovest"):  2,
    ("est",    "est"):    1,
    ("est",    "ovest"):  3,
    ("ovest",  "ovest"):  1,
}

# Limite massimo di ordini che un rider può gestire contemporaneamente
MAX_ORDINI_PER_RIDER = 2


def calcola_distanza(zona_rider: str, zona_ordine: str) -> int:
    """
    Restituisce la distanza (1, 2 o 3) tra la zona del rider e quella dell'ordine.
    Se le zone non sono nella tabella, assumiamo distanza massima (3) per sicurezza.

    Parametri:
        zona_rider  – posizione attuale del rider (es. "nord")
        zona_ordine – zona di consegna dell'ordine (es. "centro")

    Ritorna:
        int – 1, 2 o 3
    """
    # Normalizziamo in minuscolo per evitare problemi di maiuscole/minuscole
    zona_rider  = zona_rider.lower().strip()
    zona_ordine = zona_ordine.lower().strip()

    # Cerchiamo nella tabella (in entrambi gli ordini perché è simmetrica)
    if (zona_rider, zona_ordine) in DISTANZE:
        return DISTANZE[(zona_rider, zona_ordine)]
    elif (zona_ordine, zona_rider) in DISTANZE:
        return DISTANZE[(zona_ordine, zona_rider)]
    else:
        # Zona sconosciuta → distanza massima (penalità)
        return 3


def calcola_punteggio(rider: Rider, zona_ordine: str) -> int:
    """
    Calcola il punteggio di convenienza per un rider rispetto a un ordine.
    Formula: punteggio = distanza + (numeroOrdiniAttivi * 2)

    Più basso è il punteggio, più è conveniente assegnare quel rider.
    """
    distanza = calcola_distanza(rider.posizione, zona_ordine)
    carico   = rider.numeroOrdiniAttivi

    punteggio = distanza + (carico * 2)
    return punteggio


def estrai_zona(indirizzo_consegna: str) -> str:
    """
    Estrae la zona dall'indirizzo di consegna dell'ordine.
    
    In un progetto reale si userebbe un'API di geolocalizzazione.
    Qui usiamo una versione semplificata: cerchiamo parole chiave nell'indirizzo.
    
    Esempi:
        "Via Garibaldi 5, zona nord"  → "nord"
        "Piazza Duomo 1, centro"      → "centro"
        "Via Roma 22"                 → "centro" (default)
    """
    indirizzo = indirizzo_consegna.lower()

    zone_chiave = ["centro", "nord", "sud", "est", "ovest"]

    for zona in zone_chiave:
        if zona in indirizzo:
            return zona

    # Se non troviamo una zona, assumiamo "centro" come default
    return "centro"


def assegna_rider_automatico(ordine: Ordine) -> dict:
    """
    Funzione principale di assegnazione automatica.
    Implementa l'algoritmo descritto nel documento di progetto.

    Parametri:
        ordine – oggetto Ordine da assegnare

    Ritorna:
        dict con chiavi:
            "successo" (bool)
            "rider"    (dict o None)
            "messaggio" (str)
    """

    # STEP 1 – Recuperiamo i rider disponibili
    rider_disponibili = Rider.query.filter_by(stato="disponibile").all()

    # Se non ci sono rider → l'ordine resta in "pronto" e aspetta
    if not rider_disponibili:
        return {
            "successo":  False,
            "rider":     None,
            "messaggio": "Nessun rider disponibile al momento. L'ordine resta in attesa."
        }

    # Filtriamo anche per limite massimo ordini attivi
    rider_disponibili = [
        r for r in rider_disponibili
        if r.numeroOrdiniAttivi < MAX_ORDINI_PER_RIDER
    ]

    if not rider_disponibili:
        return {
            "successo":  False,
            "rider":     None,
            "messaggio": f"Tutti i rider hanno raggiunto il limite di {MAX_ORDINI_PER_RIDER} ordini attivi."
        }

    # STEP 2 – Estraiamo la zona dell'ordine dall'indirizzo
    zona_ordine = estrai_zona(ordine.indirizzoConsegna)

    # STEP 3 & 4 – Calcoliamo il punteggio per ogni rider
    # Creiamo una lista di tuple (rider, punteggio) per poi ordinarla
    rider_con_punteggio = []

    for rider in rider_disponibili:
        punteggio = calcola_punteggio(rider, zona_ordine)
        rider_con_punteggio.append((rider, punteggio))

        # Debug: stampiamo i punteggi nel terminale durante lo sviluppo
        print(f"  → Rider: {rider.nome:<10} | Zona: {rider.posizione:<8} "
              f"| Ordini attivi: {rider.numeroOrdiniAttivi} | Punteggio: {punteggio}")

    # STEP 5 – Ordiniamo per punteggio crescente
    # In caso di parità: chi ha meno ordini attivi viene prima (secondo criterio)
    rider_con_punteggio.sort(key=lambda x: (x[1], x[0].numeroOrdiniAttivi))

    # STEP 5 – Selezioniamo il migliore (primo della lista ordinata)
    miglior_rider, punteggio_min = rider_con_punteggio[0]

    # STEP 6 – Assegnazione
    ordine.idRider = miglior_rider.idRider
    ordine.stato   = "in consegna"

    miglior_rider.numeroOrdiniAttivi += 1

    # Se il rider ha ancora posti disponibili, rimane "disponibile"
    # altrimenti diventa "occupato"
    if miglior_rider.numeroOrdiniAttivi >= MAX_ORDINI_PER_RIDER:
        miglior_rider.stato = "occupato"

    db.session.commit()

    print(f"✅  Rider assegnato: {miglior_rider.nome} (punteggio: {punteggio_min})")

    return {
        "successo":  True,
        "rider":     miglior_rider.to_dict(),
        "messaggio": f"Rider {miglior_rider.nome} assegnato con punteggio {punteggio_min}",
        "dettagli": {
            "zonaOrdine":     zona_ordine,
            "zonaRider":      miglior_rider.posizione,
            "punteggio":      punteggio_min,
            "ordiniAttiviRider": miglior_rider.numeroOrdiniAttivi
        }
    }