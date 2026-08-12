"""
routes_rider.py - Rotte API per la gestione dei Rider (fattorini)

Endpoint disponibili:
  GET    /rider/                  → lista tutti i rider
  GET    /rider/disponibili       → solo i rider disponibili
  GET    /rider/<id>              → dettaglio di un rider
  POST   /rider/                  → registra un nuovo rider
  PUT    /rider/<id>              → modifica i dati di un rider
  PATCH  /rider/<id>/stato        → aggiorna lo stato (disponibile/occupato)
  PATCH  /rider/<id>/consegnato   → segnala consegna completata (libera il rider)
  DELETE /rider/<id>              → rimuove un rider
"""

from flask import Blueprint, request, jsonify
from database import db, Rider, Ordine

rider_bp = Blueprint("rider", __name__)

STATI_RIDER = ["disponibile", "occupato"]


# ── GET /rider/ ────────────────────────────────────────────────
@rider_bp.route("/", methods=["GET"])
def get_tutti_rider():
    """Restituisce la lista di tutti i rider."""
    rider = Rider.query.all()
    return jsonify([r.to_dict() for r in rider]), 200


# ── GET /rider/disponibili ─────────────────────────────────────
@rider_bp.route("/disponibili", methods=["GET"])
def get_rider_disponibili():
    """Restituisce solo i rider con stato 'disponibile'."""
    rider = Rider.query.filter_by(stato="disponibile").all()
    return jsonify([r.to_dict() for r in rider]), 200


# ── GET /rider/<id> ────────────────────────────────────────────
@rider_bp.route("/<int:id_rider>", methods=["GET"])
def get_rider(id_rider):
    """Restituisce i dettagli di un singolo rider."""
    rider = Rider.query.get_or_404(id_rider)
    return jsonify(rider.to_dict()), 200


# ── POST /rider/ ───────────────────────────────────────────────
@rider_bp.route("/", methods=["POST"])
def crea_rider():
    """
    Registra un nuovo rider nel sistema.

    Esempio di richiesta:
    {
        "nome": "Luca Bianchi",
        "telefono": "347-9876543",
        "posizione": "Centro storico",
        "mezzoDiTrasporto": "scooter"
    }
    """
    dati = request.get_json()

    if not dati or not all(k in dati for k in ("nome", "telefono")):
        return jsonify({"errore": "Campi obbligatori: nome, telefono"}), 400

    nuovo_rider = Rider(
        nome             = dati["nome"],
        telefono         = dati["telefono"],
        stato            = "disponibile",       # nuovo rider: sempre disponibile
        posizione        = dati.get("posizione", ""),
        mezzoDiTrasporto = dati.get("mezzoDiTrasporto", "")
    )

    db.session.add(nuovo_rider)
    db.session.commit()

    return jsonify(nuovo_rider.to_dict()), 201


# ── PUT /rider/<id> ────────────────────────────────────────────
@rider_bp.route("/<int:id_rider>", methods=["PUT"])
def modifica_rider(id_rider):
    """Aggiorna i dati di un rider esistente."""
    rider = Rider.query.get_or_404(id_rider)
    dati  = request.get_json()

    if not dati:
        return jsonify({"errore": "Nessun dato ricevuto"}), 400

    if "nome"             in dati: rider.nome             = dati["nome"]
    if "telefono"         in dati: rider.telefono         = dati["telefono"]
    if "posizione"        in dati: rider.posizione        = dati["posizione"]
    if "mezzoDiTrasporto" in dati: rider.mezzoDiTrasporto = dati["mezzoDiTrasporto"]

    db.session.commit()
    return jsonify(rider.to_dict()), 200


# ── PATCH /rider/<id>/stato ────────────────────────────────────
@rider_bp.route("/<int:id_rider>/stato", methods=["PATCH"])
def aggiorna_stato_rider(id_rider):
    """
    Cambia lo stato del rider (disponibile / occupato).

    Esempio: { "stato": "disponibile" }
    """
    rider = Rider.query.get_or_404(id_rider)
    dati  = request.get_json()

    if not dati or "stato" not in dati:
        return jsonify({"errore": "Campo obbligatorio: stato"}), 400

    if dati["stato"] not in STATI_RIDER:
        return jsonify({"errore": f"Stato non valido. Valori accettati: {STATI_RIDER}"}), 400

    rider.stato = dati["stato"]
    db.session.commit()

    return jsonify({
        "messaggio": f"Rider {rider.nome} ora è: {rider.stato}",
        "rider":     rider.to_dict()
    }), 200


# ── PATCH /rider/<id>/consegnato ──────────────────────────────
@rider_bp.route("/<int:id_rider>/consegnato", methods=["PATCH"])
def segna_consegnato(id_rider):
    """
    Segnala che il rider ha completato una consegna.
    - Mette l'ordine in stato 'consegnato'
    - Decrementa il contatore degli ordini attivi del rider
    - Se ha finito tutti gli ordini, lo rimette disponibile

    Esempio: { "idOrdine": 5 }
    """
    rider = Rider.query.get_or_404(id_rider)
    dati  = request.get_json()

    if not dati or "idOrdine" not in dati:
        return jsonify({"errore": "Campo obbligatorio: idOrdine"}), 400

    ordine = Ordine.query.get(dati["idOrdine"])
    if not ordine:
        return jsonify({"errore": f"Ordine {dati['idOrdine']} non trovato"}), 404

    if ordine.idRider != id_rider:
        return jsonify({"errore": "Questo ordine non appartiene a questo rider"}), 400

    # Aggiorniamo l'ordine
    ordine.stato = "consegnato"

    # Aggiorniamo il rider: decrementiamo il contatore (minimo 0)
    rider.numeroOrdiniAttivi = max(0, rider.numeroOrdiniAttivi - 1)

    # Se non ha più ordini attivi, torna disponibile
    if rider.numeroOrdiniAttivi == 0:
        rider.stato = "disponibile"

    db.session.commit()

    return jsonify({
        "messaggio":          f"Ordine #{ordine.idOrdine} consegnato!",
        "ordine":             ordine.to_dict(),
        "rider":              rider.to_dict(),
        "riderDisponibile":   rider.stato == "disponibile"
    }), 200


# ── DELETE /rider/<id> ─────────────────────────────────────────
@rider_bp.route("/<int:id_rider>", methods=["DELETE"])
def elimina_rider(id_rider):
    """
    Rimuove un rider dal sistema.
    Non è possibile eliminare un rider con ordini attivi.
    """
    rider = Rider.query.get_or_404(id_rider)

    if rider.numeroOrdiniAttivi > 0:
        return jsonify({
            "errore": f"{rider.nome} ha ancora {rider.numeroOrdiniAttivi} ordine/i attivo/i"
        }), 400

    db.session.delete(rider)
    db.session.commit()

    return jsonify({"messaggio": f"Rider {rider.nome} rimosso dal sistema"}), 200