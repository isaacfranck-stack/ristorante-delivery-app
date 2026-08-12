"""
routes_clienti.py - Rotte API per la gestione dei Clienti

Endpoint disponibili:
  GET    /clienti/          → lista tutti i clienti
  GET    /clienti/<id>      → dettaglio di un cliente
  POST   /clienti/          → crea un nuovo cliente
  PUT    /clienti/<id>      → modifica un cliente esistente
  DELETE /clienti/<id>      → elimina un cliente
"""

from flask import Blueprint, request, jsonify
from database import db, Cliente

# Un Blueprint è come un "mini-app" Flask: raggruppa rotte correlate
clienti_bp = Blueprint("clienti", __name__)


# ── GET /clienti/ ──────────────────────────────────────────────
@clienti_bp.route("/", methods=["GET"])
def get_tutti_clienti():
    """Restituisce la lista completa dei clienti."""
    clienti = Cliente.query.all()   # SELECT * FROM cliente

    # Convertiamo ogni oggetto in dizionario e poi in JSON
    return jsonify([c.to_dict() for c in clienti]), 200


# ── GET /clienti/<id> ──────────────────────────────────────────
@clienti_bp.route("/<int:id_cliente>", methods=["GET"])
def get_cliente(id_cliente):
    """Restituisce i dati di un singolo cliente cercato per ID."""

    # get_or_404: cerca per chiave primaria; se non esiste risponde automaticamente con 404
    cliente = Cliente.query.get_or_404(id_cliente)
    return jsonify(cliente.to_dict()), 200


# ── POST /clienti/ ─────────────────────────────────────────────
@clienti_bp.route("/", methods=["POST"])
def crea_cliente():
    """
    Crea un nuovo cliente.
    Il corpo della richiesta deve essere JSON con: nome, telefono, indirizzo.

    Esempio di richiesta:
    {
        "nome": "Marco Rossi",
        "telefono": "333-1234567",
        "indirizzo": "Via Roma 10, Firenze"
    }
    """
    dati = request.get_json()   # leggiamo il corpo JSON della richiesta

    # Controlliamo che tutti i campi obbligatori siano presenti
    if not dati or not all(k in dati for k in ("nome", "telefono", "indirizzo")):
        return jsonify({"errore": "Campi obbligatori: nome, telefono, indirizzo"}), 400

    nuovo_cliente = Cliente(
        nome      = dati["nome"],
        telefono  = dati["telefono"],
        indirizzo = dati["indirizzo"]
    )

    db.session.add(nuovo_cliente)   # prepariamo l'inserimento
    db.session.commit()             # salviamo nel database

    return jsonify(nuovo_cliente.to_dict()), 201   # 201 = Created


# ── PUT /clienti/<id> ──────────────────────────────────────────
@clienti_bp.route("/<int:id_cliente>", methods=["PUT"])
def modifica_cliente(id_cliente):
    """
    Aggiorna i dati di un cliente esistente.
    Si possono inviare solo i campi che si vuole modificare.
    """
    cliente = Cliente.query.get_or_404(id_cliente)
    dati    = request.get_json()

    if not dati:
        return jsonify({"errore": "Nessun dato ricevuto"}), 400

    # Aggiorniamo solo i campi presenti nel JSON (gli altri rimangono invariati)
    if "nome"      in dati: cliente.nome      = dati["nome"]
    if "telefono"  in dati: cliente.telefono  = dati["telefono"]
    if "indirizzo" in dati: cliente.indirizzo = dati["indirizzo"]

    db.session.commit()   # salviamo le modifiche

    return jsonify(cliente.to_dict()), 200


# ── DELETE /clienti/<id> ───────────────────────────────────────
@clienti_bp.route("/<int:id_cliente>", methods=["DELETE"])
def elimina_cliente(id_cliente):
    """Elimina un cliente dal database."""
    cliente = Cliente.query.get_or_404(id_cliente)

    db.session.delete(cliente)
    db.session.commit()

    return jsonify({"messaggio": f"Cliente {cliente.nome} eliminato con successo"}), 200