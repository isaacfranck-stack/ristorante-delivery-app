/*
  api.js — Modulo condiviso per le chiamate al backend Flask
  ===========================================================

  ORA CHE FLASK SERVE ANCHE LE PAGINE HTML:
  API_URL = "" (stringa vuota) perché siamo già sullo stesso server.
  fetch("/prodotti/disponibili") funziona direttamente senza CORS.
*/

const API_URL = "";   // <-- stringa vuota: stesso server Flask

// ── TOKEN JWT ──────────────────────────────────────────────────
function salvaToken(token, utente) {
  localStorage.setItem("token", token);
  localStorage.setItem("utente", JSON.stringify(utente));
}
function leggiToken()  { return localStorage.getItem("token"); }
function leggiUtente() {
  const r = localStorage.getItem("utente");
  return r ? JSON.parse(r) : null;
}
function rimuoviToken() {
  localStorage.removeItem("token");
  localStorage.removeItem("utente");
}
function eLoggato() { return leggiToken() !== null; }

// ── FUNZIONE FETCH CENTRALE ────────────────────────────────────
async function chiama(endpoint, metodo = "GET", corpo = null) {
  const headers = { "Content-Type": "application/json" };
  const token   = leggiToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const opzioni = { method: metodo, headers };
  if (corpo) opzioni.body = JSON.stringify(corpo);

  const risposta = await fetch(API_URL + endpoint, opzioni);
  const dati     = await risposta.json();

  if (!risposta.ok) throw new Error(dati.errore || "Errore del server");
  return dati;
}

// ── API PRONTI ─────────────────────────────────────────────────
const Auth = {
  registrati: (nome, email, password) =>
    chiama("/auth/registrati", "POST", { nome, email, password }),
  login: (email, password) =>
    chiama("/auth/login", "POST", { email, password }),
};

const Prodotti = {
  disponibili: () => chiama("/prodotti/disponibili"),
};

const Ordini = {
  crea: (idCliente, indirizzoConsegna, prodotti) =>
    chiama("/ordini/", "POST", { idCliente, indirizzoConsegna, prodotti }),
};

const Clienti = {
  crea: (nome, telefono, indirizzo) =>
    chiama("/clienti/", "POST", { nome, telefono, indirizzo }),
};

// ── NAVBAR ─────────────────────────────────────────────────────
function aggiornaNavabar() {
  const utente     = leggiUtente();
  const linkLogout = document.getElementById("link-logout");
  const linkLogin  = document.getElementById("link-login");
  if (utente && linkLogout) {
    linkLogout.style.display = "inline";
    linkLogout.textContent   = `Esci (${utente.nome.split(" ")[0]})`;
    if (linkLogin) linkLogin.style.display = "none";
  }
}

function logout() {
  rimuoviToken();
  window.location.href = "/";
}