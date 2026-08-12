"""
database.py - Configurazione e creazione del database

Questo file si occupa di:
1. Creare la connessione al database SQLite
2. Definire tutte le tabelle (tramite SQLAlchemy)
3. Popolare il menu iniziale al primo avvio
4. Inserire i 5 rider del ristorante
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ─────────────────────────────────────────────
#  MODELLI (= Tabelle del database)
# ─────────────────────────────────────────────

class Cliente(db.Model):
    """Rappresenta un cliente della trattoria."""
    __tablename__ = "cliente"

    idCliente   = db.Column(db.Integer, primary_key=True)
    nome        = db.Column(db.String(100), nullable=False)
    telefono    = db.Column(db.String(20),  nullable=False)
    indirizzo   = db.Column(db.String(200), nullable=False)

    ordini = db.relationship("Ordine", backref="cliente", lazy=True)

    def to_dict(self):
        return {
            "idCliente": self.idCliente,
            "nome":      self.nome,
            "telefono":  self.telefono,
            "indirizzo": self.indirizzo
        }


class Prodotto(db.Model):
    """Rappresenta una voce del menu."""
    __tablename__ = "prodotto"

    idProdotto  = db.Column(db.Integer, primary_key=True)
    nome        = db.Column(db.String(100), nullable=False)
    descrizione = db.Column(db.String(300))
    prezzo      = db.Column(db.Float,       nullable=False)
    disponibile = db.Column(db.Boolean,     default=True)

    def to_dict(self):
        return {
            "idProdotto":  self.idProdotto,
            "nome":        self.nome,
            "descrizione": self.descrizione,
            "prezzo":      self.prezzo,
            "disponibile": self.disponibile
        }


class Rider(db.Model):
    """
    Rappresenta un fattorino.
    Posizione = zona della citta (centro, nord, sud, est, ovest).
    """
    __tablename__ = "rider"

    idRider             = db.Column(db.Integer, primary_key=True)
    nome                = db.Column(db.String(100), nullable=False)
    telefono            = db.Column(db.String(20),  nullable=False)
    stato               = db.Column(db.String(20),  default="disponibile")
    numeroOrdiniAttivi  = db.Column(db.Integer,     default=0)
    posizione           = db.Column(db.String(100))   # zona: centro, nord, sud, est, ovest
    mezzoDiTrasporto    = db.Column(db.String(50))    # auto, fat-bike, moto

    ordini = db.relationship("Ordine", backref="rider", lazy=True)

    def to_dict(self):
        return {
            "idRider":            self.idRider,
            "nome":               self.nome,
            "telefono":           self.telefono,
            "stato":              self.stato,
            "numeroOrdiniAttivi": self.numeroOrdiniAttivi,
            "posizione":          self.posizione,
            "mezzoDiTrasporto":   self.mezzoDiTrasporto
        }


class Ordine(db.Model):
    """
    Rappresenta un ordine effettuato da un cliente.

    Flusso degli stati:
    ricevuto -> in preparazione -> pronto -> in consegna -> consegnato
                                          (assegnazione automatica rider)
    oppure -> annullato
    """
    __tablename__ = "ordine"

    idOrdine          = db.Column(db.Integer, primary_key=True)
    data              = db.Column(db.DateTime, default=datetime.utcnow)
    stato             = db.Column(db.String(30), default="ricevuto")
    totale            = db.Column(db.Float,   default=0.0)
    indirizzoConsegna = db.Column(db.String(200), nullable=False)

    idCliente = db.Column(db.Integer, db.ForeignKey("cliente.idCliente"), nullable=False)
    idRider   = db.Column(db.Integer, db.ForeignKey("rider.idRider"),     nullable=True)

    dettagli = db.relationship("DettaglioOrdine", backref="ordine", lazy=True)

    def to_dict(self):
        return {
            "idOrdine":          self.idOrdine,
            "data":              self.data.strftime("%Y-%m-%d %H:%M"),
            "stato":             self.stato,
            "totale":            self.totale,
            "indirizzoConsegna": self.indirizzoConsegna,
            "idCliente":         self.idCliente,
            "idRider":           self.idRider
        }


class DettaglioOrdine(db.Model):
    """
    Tabella ponte N:M tra Ordine e Prodotto.
    Salviamo il prezzoUnitario al momento dell'ordine per mantenere lo storico corretto.
    """
    __tablename__ = "dettaglio_ordine"

    idDettaglio    = db.Column(db.Integer, primary_key=True)
    quantita       = db.Column(db.Integer, nullable=False, default=1)
    prezzoUnitario = db.Column(db.Float,   nullable=False)

    idOrdine   = db.Column(db.Integer, db.ForeignKey("ordine.idOrdine"),     nullable=False)
    idProdotto = db.Column(db.Integer, db.ForeignKey("prodotto.idProdotto"), nullable=False)

    prodotto = db.relationship("Prodotto")

    def to_dict(self):
        return {
            "idDettaglio":    self.idDettaglio,
            "idOrdine":       self.idOrdine,
            "idProdotto":     self.idProdotto,
            "nomeProdotto":   self.prodotto.nome if self.prodotto else None,
            "quantita":       self.quantita,
            "prezzoUnitario": self.prezzoUnitario,
            "subtotale":      round(self.quantita * self.prezzoUnitario, 2)
        }


# ─────────────────────────────────────────────
#  POPOLAMENTO INIZIALE DEL MENU
# ─────────────────────────────────────────────

def popola_menu():
    """Inserisce i piatti del menu se non esistono gia."""
    if Prodotto.query.count() > 0:
        return

    menu = [
        Prodotto(nome="Pappardelle al Cinghiale",
                 descrizione="Strati di pasta fresca, ragu di carne, besciamella e Parmigiano Reggiano",
                 prezzo=14.00),
        Prodotto(nome="Ribollita Toscana",
                 descrizione="Zuppa rustica di pane, cavolo nero, fagioli cannellini e verdure",
                 prezzo=10.00),
        Prodotto(nome="Pici all'Aglione",
                 descrizione="Pasta fatta a mano con sugo di pomodoro e aglio",
                 prezzo=12.00),
        Prodotto(nome="Minestrone della Nonna",
                 descrizione="Zuppa di verdure stagionali, fagioli borlotti e pasta mista",
                 prezzo=9.50),
        Prodotto(nome="Gnocchi di Patate al Ragu",
                 descrizione="Gnocchi freschi con ragu di carne di manzo e maiale",
                 prezzo=13.00),
        Prodotto(nome="Risotto alla Pilota",
                 descrizione="Risotto mantovano con salsiccia, burro e parmigiano",
                 prezzo=13.50),
        Prodotto(nome="Spezzatino di Manzo con Polenta",
                 descrizione="Carne di manzo brasata con verdure, servita con polenta morbida",
                 prezzo=16.00),
        Prodotto(nome="Cotechino con Lenticchie",
                 descrizione="Cotechino Modena IGP con lenticchie di Castelluccio",
                 prezzo=15.00),
        Prodotto(nome="Pollo in Potacchio",
                 descrizione="Pollo alla cacciatora in bianco con rosmarino, vino e aglio",
                 prezzo=13.50),
        Prodotto(nome="Baccala alla Livornese",
                 descrizione="Filetti di baccala con pomodoro, olive nere e capperi",
                 prezzo=15.00),
        Prodotto(nome="Trippa alla Fiorentina",
                 descrizione="Trippa in umido con pomodoro, parmigiano e crostini di pane",
                 prezzo=12.00),
        Prodotto(nome="Salsicce e Fagioli",
                 descrizione="Salsicce di maiale alla griglia con fagioli borlotti all'olio",
                 prezzo=14.00),
        Prodotto(nome="Tiramisu della Nonna",
                 descrizione="Savoiardi, mascarpone, caffe, cacao amaro (in vasetto monoporzione)",
                 prezzo=5.00),
        Prodotto(nome="Torta Caprese",
                 descrizione="Torta al cioccolato fondente e mandorle, originaria di Capri",
                 prezzo=5.50),
        Prodotto(nome="Cantucci con Vin Santo",
                 descrizione="Biscotti alle mandorle tipici toscani con vino liquoroso",
                 prezzo=4.50),
        Prodotto(nome="Acqua Naturale 33cl",  descrizione="", prezzo=1.50),
        Prodotto(nome="Acqua Frizzante 33cl", descrizione="", prezzo=1.50),
        Prodotto(nome="Heineken 66cl",        descrizione="", prezzo=5.50),
    ]

    db.session.add_all(menu)
    db.session.commit()
    print("Menu inserito nel database!")


# ─────────────────────────────────────────────
#  POPOLAMENTO INIZIALE DEI RIDER
# ─────────────────────────────────────────────

def popola_rider():
    """
    Inserisce i 5 rider del ristorante se non esistono gia.

    Assegnazione mezzi e zone:
    - Franck  -> Auto      -> centro  (comoda per i bagagli piu grandi)
    - Ibty    -> Moto      -> nord    (veloce sulle strade trafficate)
    - Sara    -> Fat-bike  -> sud     (ecologica per zona piu tranquilla)
    - Pooria  -> Moto      -> est     (rapido per coprire la zona est)
    - Marsila -> Fat-bike  -> ovest   (zona residenziale, ideale per la bici)
    """
    if Rider.query.count() > 0:
        return

    rider_iniziali = [
        Rider(nome="Franck",  telefono="333-1000001", stato="disponibile",
              numeroOrdiniAttivi=0, posizione="centro", mezzoDiTrasporto="auto"),
        Rider(nome="Ibty",    telefono="333-1000002", stato="disponibile",
              numeroOrdiniAttivi=0, posizione="nord",   mezzoDiTrasporto="moto"),
        Rider(nome="Sara",    telefono="333-1000003", stato="disponibile",
              numeroOrdiniAttivi=0, posizione="sud",    mezzoDiTrasporto="fat-bike"),
        Rider(nome="Pooria",  telefono="333-1000004", stato="disponibile",
              numeroOrdiniAttivi=0, posizione="est",    mezzoDiTrasporto="moto"),
        Rider(nome="Marsila", telefono="333-1000005", stato="disponibile",
              numeroOrdiniAttivi=0, posizione="ovest",  mezzoDiTrasporto="fat-bike"),
    ]

    db.session.add_all(rider_iniziali)
    db.session.commit()
    print("5 Rider inseriti: Franck(auto/centro), Ibty(moto/nord), Sara(fat-bike/sud), Pooria(moto/est), Marsila(fat-bike/ovest)")


# ─────────────────────────────────────────────
#  MODELLO UTENTE PER L'AUTENTICAZIONE
# ─────────────────────────────────────────────

class UtenteAuth(db.Model):
    """
    Rappresenta un account utente con email e password.

    Nota: questa tabella e' SEPARATA dalla tabella Cliente.
    Un Cliente e' chi fa un ordine (con nome, telefono, indirizzo).
    Un UtenteAuth e' chi ha un account con email e password.
    In un progetto piu' avanzato si potrebbero collegare,
    ma per ora le teniamo separate per semplicita'.

    Il campo 'ruolo' serve per distinguere:
    - "cliente"  -> puo' vedere il menu e fare ordini
    - "staff"    -> puo' aggiornare gli stati degli ordini
    - "admin"    -> puo' fare tutto (gestire menu, rider, ecc.)
    """
    __tablename__ = "utente_auth"

    id            = db.Column(db.Integer, primary_key=True)
    nome          = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(150), unique=True, nullable=False)  # unique: no duplicati
    password_hash = db.Column(db.String(200), nullable=False)               # mai la password vera!
    ruolo         = db.Column(db.String(20),  default="cliente")            # cliente / staff / admin

    def to_dict(self):
        return {
            "id":    self.id,
            "nome":  self.nome,
            "email": self.email,
            "ruolo": self.ruolo
            # NOTA: non includiamo mai password_hash nella risposta!
        }