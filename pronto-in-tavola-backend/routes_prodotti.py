"""
routes_prodotti.py - Rotte API per la gestione dei Prodotti (menu)

Endpoint disponibili:
  GET    /prodotti/              → lista tutto il menu
  GET    /prodotti/disponibili   → solo i piatti disponibili oggi
  GET    /prodotti/<id>          → dettaglio di un prodotto
  POST   /prodotti/              → aggiunge un nuovo piatto al menu
  PUT    /prodotti/<id>          → modifica un piatto
  PATCH  /prodotti/<id>/disponibilita → cambia solo la disponibilità
  DELETE /prodotti/<id>          → rimuove un piatto dal menu
"""

from flask import Blueprint, request, jsonify
from database import db, Prodotto

prodotti_bp = Blueprint("prodotti", __name__)


# ── GET /prodotti/ ─────────────────────────────────────────────
@prodotti_bp.route("/", methods=["GET"])
def get_tutti_prodotti():
    """Restituisce l'intero menu (disponibili e non)."""
    prodotti = Prodotto.query.all()
    return jsonify([p.to_dict() for p in prodotti]), 200


# ── GET /prodotti/disponibili ──────────────────────────────────
@prodotti_bp.route("/disponibili", methods=["GET"])
def get_prodotti_disponibili():
    """
    Restituisce solo i piatti attualmente disponibili.
    Utile per mostrare il menu aggiornato ai clienti.
    """
    # Filtriamo con WHERE disponibile = True
    prodotti = Prodotto.query.filter_by(disponibile=True).all()
    return jsonify([p.to_dict() for p in prodotti]), 200


# ── GET /prodotti/<id> ─────────────────────────────────────────
@prodotti_bp.route("/<int:id_prodotto>", methods=["GET"])
def get_prodotto(id_prodotto):
    """Restituisce i dettagli di un singolo piatto."""
    prodotto = Prodotto.query.get_or_404(id_prodotto)
    return jsonify(prodotto.to_dict()), 200


# ── POST /prodotti/ ────────────────────────────────────────────
@prodotti_bp.route("/", methods=["POST"])
def crea_prodotto():
    """
    Aggiunge un nuovo piatto al menu.

    Esempio di richiesta:
    {
        "nome": "Bistecca alla Fiorentina",
        "descrizione": "T-bone di chianina, minimo 800g",
        "prezzo": 28.00,
        "disponibile": true
    }
    """
    dati = request.get_json()

    if not dati or "nome" not in dati or "prezzo" not in dati:
        return jsonify({"errore": "Campi obbligatori: nome, prezzo"}), 400

    # Verifichiamo che il prezzo sia un numero positivo
    try:
        prezzo = float(dati["prezzo"])
        if prezzo < 0:
            raise ValueError()
    except (ValueError, TypeError):
        return jsonify({"errore": "Il prezzo deve essere un numero positivo"}), 400

    nuovo = Prodotto(
        nome        = dati["nome"],
        descrizione = dati.get("descrizione", ""),   # .get() usa "" se non specificato
        prezzo      = prezzo,
        disponibile = dati.get("disponibile", True)  # default: disponibile
    )

    db.session.add(nuovo)
    db.session.commit()

    return jsonify(nuovo.to_dict()), 201


# ── PUT /prodotti/<id> ─────────────────────────────────────────
@prodotti_bp.route("/<int:id_prodotto>", methods=["PUT"])
def modifica_prodotto(id_prodotto):
    """Modifica i dati di un piatto del menu."""
    prodotto = Prodotto.query.get_or_404(id_prodotto)
    dati     = request.get_json()

    if not dati:
        return jsonify({"errore": "Nessun dato ricevuto"}), 400

    if "nome"        in dati: prodotto.nome        = dati["nome"]
    if "descrizione" in dati: prodotto.descrizione = dati["descrizione"]
    if "disponibile" in dati: prodotto.disponibile = dati["disponibile"]

    if "prezzo" in dati:
        try:
            prodotto.prezzo = float(dati["prezzo"])
        except (ValueError, TypeError):
            return jsonify({"errore": "Il prezzo deve essere un numero"}), 400

    db.session.commit()
    return jsonify(prodotto.to_dict()), 200


# ── PATCH /prodotti/<id>/disponibilita ────────────────────────
@prodotti_bp.route("/<int:id_prodotto>/disponibilita", methods=["PATCH"])
def cambia_disponibilita(id_prodotto):
    """
    Endpoint dedicato per attivare/disattivare un piatto.
    PATCH modifica solo una parte della risorsa (a differenza di PUT che la sostituisce).

    Esempio: { "disponibile": false }  → piatto non disponibile oggi
    """
    prodotto = Prodotto.query.get_or_404(id_prodotto)
    dati     = request.get_json()

    if dati is None or "disponibile" not in dati:
        return jsonify({"errore": "Campo obbligatorio: disponibile (true/false)"}), 400

    prodotto.disponibile = bool(dati["disponibile"])
    db.session.commit()

    stato = "disponibile" if prodotto.disponibile else "non disponibile"
    return jsonify({
        "messaggio": f"'{prodotto.nome}' è ora {stato}",
        "prodotto":  prodotto.to_dict()
    }), 200


# ── DELETE /prodotti/<id> ──────────────────────────────────────
@prodotti_bp.route("/<int:id_prodotto>", methods=["DELETE"])
def elimina_prodotto(id_prodotto):
    """Rimuove definitivamente un piatto dal menu."""
    prodotto = Prodotto.query.get_or_404(id_prodotto)
    db.session.delete(prodotto)
    db.session.commit()
    return jsonify({"messaggio": f"Prodotto '{prodotto.nome}' eliminato"}), 200