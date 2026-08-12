"""
routes_auth.py - Registrazione e Login degli utenti

Endpoint disponibili:
  POST /auth/registrati   -> crea un nuovo account utente
  POST /auth/login        -> accede con email e password, riceve un token JWT
  GET  /auth/profilo      -> legge i dati dell'utente loggato (richiede token)

Cos'e' un token JWT?
  E' una stringa cifrata che il server genera al login.
  Il frontend la conserva (es. nel localStorage) e la manda
  in ogni richiesta nell'header:  Authorization: Bearer <token>
  Cosi' il server sa chi sta facendo la richiesta senza dover
  chiedere di nuovo la password ogni volta.

Cos'e' bcrypt?
  E' un algoritmo che trasforma la password in una stringa
  illeggibile (es. "$2b$12$xK9..."). Non e' reversibile:
  non si puo' risalire alla password originale.
  Si salva solo l'hash nel database, mai la password vera.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,   # genera il token JWT
    jwt_required,          # decoratore: blocca se non c'e' token valido
    get_jwt_identity       # legge l'id dell'utente dal token
)
from database import db, UtenteAuth
import bcrypt

auth_bp = Blueprint("auth", __name__)


# ── POST /auth/registrati ─────────────────────────────────────
@auth_bp.route("/registrati", methods=["POST"])
def registrati():
    """
    Crea un nuovo account utente.

    Esempio di richiesta JSON:
    {
        "nome":     "Marco Rossi",
        "email":    "marco@email.com",
        "password": "miaPassword123"
    }
    """
    dati = request.get_json()

    # Validiamo i campi obbligatori
    if not dati or not all(k in dati for k in ("nome", "email", "password")):
        return jsonify({"errore": "Campi obbligatori: nome, email, password"}), 400

    # Controlliamo che l'email non sia gia' registrata
    # (ogni utente deve avere un'email unica)
    if UtenteAuth.query.filter_by(email=dati["email"]).first():
        return jsonify({"errore": "Email gia' registrata"}), 409  # 409 = Conflict

    # Controlliamo che la password abbia almeno 6 caratteri
    if len(dati["password"]) < 6:
        return jsonify({"errore": "La password deve avere almeno 6 caratteri"}), 400

    # Cifriamo la password con bcrypt
    # encode("utf-8") converte la stringa in bytes (bcrypt lo richiede)
    # bcrypt.gensalt() genera un "sale" casuale (rende ogni hash diverso)
    password_hash = bcrypt.hashpw(
        dati["password"].encode("utf-8"),
        bcrypt.gensalt()
    )

    # Creiamo il nuovo utente con la password gia' cifrata
    nuovo_utente = UtenteAuth(
        nome          = dati["nome"],
        email         = dati["email"],
        password_hash = password_hash.decode("utf-8")  # salviamo come stringa
    )

    db.session.add(nuovo_utente)
    db.session.commit()

    return jsonify({
        "messaggio": f"Benvenuto {nuovo_utente.nome}! Account creato con successo.",
        "utente": {
            "id":    nuovo_utente.id,
            "nome":  nuovo_utente.nome,
            "email": nuovo_utente.email
        }
    }), 201  # 201 = Created


# ── POST /auth/login ──────────────────────────────────────────
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Accede con email e password.
    Se le credenziali sono corrette, restituisce un token JWT.

    Esempio di richiesta JSON:
    {
        "email":    "marco@email.com",
        "password": "miaPassword123"
    }

    Risposta in caso di successo:
    {
        "token": "eyJhbGciOiJIUzI1NiIs...",
        "utente": { "id": 1, "nome": "Marco Rossi", "email": "..." }
    }
    """
    dati = request.get_json()

    if not dati or not all(k in dati for k in ("email", "password")):
        return jsonify({"errore": "Campi obbligatori: email, password"}), 400

    # Cerchiamo l'utente nel database tramite email
    utente = UtenteAuth.query.filter_by(email=dati["email"]).first()

    # Sicurezza: se l'utente non esiste O la password e' sbagliata,
    # diamo lo stesso messaggio generico. Cosi' non riveliamo
    # se l'email e' registrata o no (protezione contro attacchi "email enumeration")
    if not utente:
        return jsonify({"errore": "Credenziali non valide"}), 401

    # Verifichiamo la password confrontando con l'hash salvato
    # bcrypt.checkpw() fa il confronto in modo sicuro
    password_corretta = bcrypt.checkpw(
        dati["password"].encode("utf-8"),
        utente.password_hash.encode("utf-8")
    )

    if not password_corretta:
        return jsonify({"errore": "Credenziali non valide"}), 401  # 401 = Unauthorized

    # Tutto ok! Generiamo il token JWT.
    # identity e' l'informazione che mettiamo "dentro" il token.
    # Usiamo l'id dell'utente (come stringa, JWT lo richiede).
    token = create_access_token(identity=str(utente.id))

    return jsonify({
        "messaggio": f"Benvenuto, {utente.nome}!",
        "token": token,   # il frontend deve conservare questo!
        "utente": {
            "id":    utente.id,
            "nome":  utente.nome,
            "email": utente.email,
            "ruolo": utente.ruolo
        }
    }), 200


# ── GET /auth/profilo ─────────────────────────────────────────
@auth_bp.route("/profilo", methods=["GET"])
@jwt_required()   # <-- questo decoratore blocca la richiesta se non c'e' token valido
def profilo():
    """
    Restituisce i dati dell'utente attualmente loggato.
    Richiede il token JWT nell'header:
        Authorization: Bearer <token>

    Questa rotta dimostra come proteggere un endpoint con il login.
    """
    # get_jwt_identity() legge l'id che avevamo messo nel token
    id_utente = get_jwt_identity()

    utente = UtenteAuth.query.get(int(id_utente))

    if not utente:
        return jsonify({"errore": "Utente non trovato"}), 404

    return jsonify({
        "id":    utente.id,
        "nome":  utente.nome,
        "email": utente.email,
        "ruolo": utente.ruolo
    }), 200