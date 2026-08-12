"""
app.py - Punto di ingresso dell'applicazione Flask

STRUTTURA DELLE CARTELLE:
  food-delivery/
  ├── app.py
  ├── templates/        ← pagine HTML (Flask le cerca qui)
  │   ├── index.html
  │   ├── login.html
  │   ├── menu.html
  │   └── carrello.html
  └── static/           ← CSS e JS (Flask li serve da qui)
      ├── stile.css
      └── api.js

COME FUNZIONA:
  Prima aprivi index.html direttamente come file (file://)
  e il browser bloccava le chiamate a Flask (origini diverse).

  Ora Flask serve sia le pagine HTML sia le API:
    http://127.0.0.1:5000/          → index.html
    http://127.0.0.1:5000/menu      → menu.html
    http://127.0.0.1:5000/prodotti/ → API JSON

  Tutto sulla stessa origine → nessun problema CORS!
"""

from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from datetime import timedelta

from database import db, popola_menu, popola_rider
from routes_auth     import auth_bp
from routes_clienti  import clienti_bp
from routes_prodotti import prodotti_bp
from routes_ordini   import ordini_bp
from routes_rider    import rider_bp


def crea_app():
    app = Flask(__name__)

    # ── Configurazione ──────────────────────────────────────────
    app.config["SQLALCHEMY_DATABASE_URI"]    = "sqlite:///trattoria.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"]             = "pronto-in-tavola-chiave-segreta-2024"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"]   = timedelta(hours=24)

    # ── Estensioni ──────────────────────────────────────────────
    db.init_app(app)
    JWTManager(app)

    # ── Rotte API (Blueprint) ───────────────────────────────────
    app.register_blueprint(auth_bp,     url_prefix="/auth")
    app.register_blueprint(clienti_bp,  url_prefix="/clienti")
    app.register_blueprint(prodotti_bp, url_prefix="/prodotti")
    app.register_blueprint(ordini_bp,   url_prefix="/ordini")
    app.register_blueprint(rider_bp,    url_prefix="/rider")

    # ── Rotte PAGINE HTML ───────────────────────────────────────
    # render_template() cerca il file dentro la cartella /templates/
    # e lo manda al browser come pagina HTML.

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/menu")
    def menu():
        return render_template("menu.html")

    @app.route("/carrello")
    def carrello():
        return render_template("carrello.html")

    # ── Database ────────────────────────────────────────────────
    with app.app_context():
        db.create_all()
        popola_menu()
        popola_rider()

    return app


if __name__ == "__main__":
    app = crea_app()
    print("")
    print("  Pronto a Tavola - Server avviato!")
    print("  Apri nel browser: http://127.0.0.1:5000")
    print("")
    app.run(debug=True)