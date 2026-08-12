"""
routes_ordini.py - Rotte API per la gestione degli Ordini

Endpoint disponibili:
  GET    /ordini/                     -> lista tutti gli ordini (filtrabili per stato)
  GET    /ordini/<id>                 -> dettaglio ordine con i prodotti
  GET    /ordini/cliente/<id_cliente> -> ordini di un cliente specifico
  POST   /ordini/                     -> crea un nuovo ordine
  PATCH  /ordini/<id>/stato           -> aggiorna lo stato dell'ordine
                                         (quando diventa "pronto", il rider viene
                                          assegnato automaticamente)
  PATCH  /ordini/<id>/assegna-rider   -> assegnazione manuale di un rider
  DELETE /ordini/<id>                 -> elimina un ordine (solo se in stato "ricevuto")

Flusso degli stati:
  ricevuto -> in preparazione -> pronto -> in consegna -> consegnato
                                        ^
                              qui scatta l'assegnazione automatica del rider
"""

from flask import Blueprint, request, jsonify
from database import db, Ordine, DettaglioOrdine, Prodotto, Cliente, Rider
from assegnazione_rider import assegna_rider_automatico

ordini_bp = Blueprint("ordini", __name__)

# Tutti gli stati validi per un ordine, nell'ordine temporale corretto
STATI_VALIDI = [
    "ricevuto",
    "in preparazione",
    "pronto",           # <-- NUOVO: l'ordine e' pronto in cucina, attende il rider
    "in consegna",
    "consegnato",
    "annullato"
]


# ── GET /ordini/ ───────────────────────────────────────────────
@ordini_bp.route("/", methods=["GET"])
def get_tutti_ordini():
    """
    Restituisce tutti gli ordini.
    Supporta il filtro per stato tramite query string:
      /ordini/?stato=pronto
      /ordini/?stato=in consegna
    """
    stato_filtro = request.args.get("stato")

    if stato_filtro:
        ordini = Ordine.query.filter_by(stato=stato_filtro).all()
    else:
        ordini = Ordine.query.all()

    return jsonify([o.to_dict() for o in ordini]), 200


# ── GET /ordini/<id> ───────────────────────────────────────────
@ordini_bp.route("/<int:id_ordine>", methods=["GET"])
def get_ordine(id_ordine):
    """
    Restituisce il dettaglio completo di un ordine,
    inclusi tutti i prodotti ordinati con quantita e subtotale.
    """
    ordine = Ordine.query.get_or_404(id_ordine)

    risposta = ordine.to_dict()
    risposta["prodotti"] = [d.to_dict() for d in ordine.dettagli]

    return jsonify(risposta), 200


# ── GET /ordini/cliente/<id_cliente> ──────────────────────────
@ordini_bp.route("/cliente/<int:id_cliente>", methods=["GET"])
def get_ordini_cliente(id_cliente):
    """Restituisce tutti gli ordini di un cliente specifico."""
    Cliente.query.get_or_404(id_cliente)   # verifichiamo che il cliente esista
    ordini = Ordine.query.filter_by(idCliente=id_cliente).all()
    return jsonify([o.to_dict() for o in ordini]), 200


# ── POST /ordini/ ──────────────────────────────────────────────
@ordini_bp.route("/", methods=["POST"])
def crea_ordine():
    """
    Crea un nuovo ordine con i relativi prodotti.
    Il totale viene calcolato automaticamente dal server.

    Esempio di richiesta JSON:
    {
        "idCliente": 1,
        "indirizzoConsegna": "Via Garibaldi 5, zona nord",
        "prodotti": [
            {"idProdotto": 1, "quantita": 2},
            {"idProdotto": 13, "quantita": 1}
        ]
    }

    Nota: l'indirizzo di consegna puo contenere la zona (es. "zona nord", "centro")
    cosi il sistema di assegnazione rider puo calcolare la distanza correttamente.
    """
    dati = request.get_json()

    if not dati:
        return jsonify({"errore": "Corpo della richiesta mancante"}), 400

    campi_obbligatori = ("idCliente", "indirizzoConsegna", "prodotti")
    if not all(k in dati for k in campi_obbligatori):
        return jsonify({"errore": f"Campi obbligatori: {', '.join(campi_obbligatori)}"}), 400

    if not isinstance(dati["prodotti"], list) or len(dati["prodotti"]) == 0:
        return jsonify({"errore": "La lista prodotti non puo essere vuota"}), 400

    # Verifichiamo che il cliente esista
    cliente = Cliente.query.get(dati["idCliente"])
    if not cliente:
        return jsonify({"errore": f"Cliente {dati['idCliente']} non trovato"}), 404

    # Creiamo l'ordine (senza totale ancora)
    nuovo_ordine = Ordine(
        idCliente        = dati["idCliente"],
        indirizzoConsegna= dati["indirizzoConsegna"],
        stato            = "ricevuto"
    )
    db.session.add(nuovo_ordine)
    db.session.flush()   # otteniamo l'idOrdine senza fare commit definitivo

    # Elaboriamo ogni prodotto della lista
    totale = 0.0

    for voce in dati["prodotti"]:
        if "idProdotto" not in voce:
            db.session.rollback()
            return jsonify({"errore": "Ogni voce deve avere 'idProdotto'"}), 400

        quantita = int(voce.get("quantita", 1))
        if quantita <= 0:
            db.session.rollback()
            return jsonify({"errore": "La quantita deve essere almeno 1"}), 400

        prodotto = Prodotto.query.get(voce["idProdotto"])
        if not prodotto:
            db.session.rollback()
            return jsonify({"errore": f"Prodotto {voce['idProdotto']} non trovato"}), 404

        if not prodotto.disponibile:
            db.session.rollback()
            return jsonify({"errore": f"'{prodotto.nome}' non e' disponibile oggi"}), 400

        # Creiamo la riga nella tabella ponte DettaglioOrdine
        dettaglio = DettaglioOrdine(
            idOrdine       = nuovo_ordine.idOrdine,
            idProdotto     = prodotto.idProdotto,
            quantita       = quantita,
            prezzoUnitario = prodotto.prezzo   # salviamo il prezzo attuale
        )
        db.session.add(dettaglio)
        totale += prodotto.prezzo * quantita

    nuovo_ordine.totale = round(totale, 2)
    db.session.commit()

    risposta = nuovo_ordine.to_dict()
    risposta["prodotti"] = [d.to_dict() for d in nuovo_ordine.dettagli]

    return jsonify(risposta), 201


# ── PATCH /ordini/<id>/stato ───────────────────────────────────
@ordini_bp.route("/<int:id_ordine>/stato", methods=["PATCH"])
def aggiorna_stato(id_ordine):
    """
    Aggiorna lo stato dell'ordine.

    ATTENZIONE: quando lo stato diventa "pronto",
    il sistema tenta automaticamente di assegnare un rider.

    Flusso completo:
      ricevuto -> in preparazione -> pronto -> (auto) in consegna -> consegnato

    Esempio: { "stato": "pronto" }
    """
    ordine = Ordine.query.get_or_404(id_ordine)
    dati   = request.get_json()

    if not dati or "stato" not in dati:
        return jsonify({"errore": "Campo obbligatorio: stato"}), 400

    nuovo_stato = dati["stato"]

    if nuovo_stato not in STATI_VALIDI:
        return jsonify({
            "errore": f"Stato '{nuovo_stato}' non valido.",
            "validi": STATI_VALIDI
        }), 400

    ordine.stato = nuovo_stato
    db.session.commit()

    risposta = {
        "messaggio": f"Ordine #{id_ordine} aggiornato a '{nuovo_stato}'",
        "ordine":    ordine.to_dict()
    }

    # ── ASSEGNAZIONE AUTOMATICA RIDER ──────────────────────────
    # Quando la cucina segna l'ordine come "pronto",
    # il sistema cerca il rider migliore e lo assegna automaticamente.
    if nuovo_stato == "pronto":
        print(f"Ordine #{id_ordine} e' PRONTO. Avvio assegnazione automatica rider...")

        risultato = assegna_rider_automatico(ordine)

        # Aggiungiamo le info sull'assegnazione alla risposta
        risposta["assegnazione_rider"] = risultato

        if risultato["successo"]:
            # Ricarichiamo l'ordine dal db per avere i dati aggiornati
            db.session.refresh(ordine)
            risposta["ordine"] = ordine.to_dict()
            risposta["messaggio"] += f" → Rider assegnato: {risultato['rider']['nome']}"
        else:
            risposta["messaggio"] += " → Nessun rider disponibile, ordine in attesa."

    return jsonify(risposta), 200


# ── PATCH /ordini/<id>/assegna-rider ──────────────────────────
@ordini_bp.route("/<int:id_ordine>/assegna-rider", methods=["PATCH"])
def assegna_rider_manuale(id_ordine):
    """
    Assegnazione MANUALE di un rider (override dello staff).
    Utile quando l'assegnazione automatica non ha trovato rider
    oppure si vuole forzare un rider specifico.

    Esempio: { "idRider": 2 }
    """
    ordine = Ordine.query.get_or_404(id_ordine)
    dati   = request.get_json()

    if not dati or "idRider" not in dati:
        return jsonify({"errore": "Campo obbligatorio: idRider"}), 400

    rider = Rider.query.get(dati["idRider"])
    if not rider:
        return jsonify({"errore": f"Rider {dati['idRider']} non trovato"}), 404

    if rider.stato != "disponibile":
        return jsonify({"errore": f"Il rider {rider.nome} non e' disponibile"}), 400

    # Assegniamo il rider manualmente
    ordine.idRider = rider.idRider
    ordine.stato   = "in consegna"

    rider.stato              = "occupato"
    rider.numeroOrdiniAttivi += 1

    db.session.commit()

    return jsonify({
        "messaggio": f"Rider {rider.nome} assegnato manualmente all'ordine #{id_ordine}",
        "ordine":    ordine.to_dict(),
        "rider":     rider.to_dict()
    }), 200


# ── DELETE /ordini/<id> ────────────────────────────────────────
@ordini_bp.route("/<int:id_ordine>", methods=["DELETE"])
def elimina_ordine(id_ordine):
    """
    Elimina un ordine solo se e' ancora in stato 'ricevuto'.
    Non si puo cancellare un ordine gia in preparazione o in consegna.
    """
    ordine = Ordine.query.get_or_404(id_ordine)

    if ordine.stato != "ricevuto":
        return jsonify({
            "errore": f"Non puoi eliminare un ordine in stato '{ordine.stato}'"
        }), 400

    for dettaglio in ordine.dettagli:
        db.session.delete(dettaglio)

    db.session.delete(ordine)
    db.session.commit()

    return jsonify({"messaggio": f"Ordine #{id_ordine} eliminato"}), 200