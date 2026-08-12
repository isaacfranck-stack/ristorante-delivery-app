export interface UtenteInfo {
  id: number
  nome: string
  email: string
  ruolo: string
}

export function salvaToken(token: string, utente: UtenteInfo): void {
  localStorage.setItem('token', token)
  localStorage.setItem('utente', JSON.stringify(utente))
}

export function leggiToken(): string | null {
  return localStorage.getItem('token')
}

export function leggiUtente(): UtenteInfo | null {
  const raw = localStorage.getItem('utente')
  return raw ? JSON.parse(raw) : null
}

export function rimuoviToken(): void {
  localStorage.removeItem('token')
  localStorage.removeItem('utente')
}

export function eLoggato(): boolean {
  return leggiToken() !== null
}

async function chiama<T>(endpoint: string, metodo = 'GET', corpo?: unknown): Promise<T> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  const token = leggiToken()
  if (token) headers['Authorization'] = `Bearer ${token}`

  const opzioni: RequestInit = { method: metodo, headers }
  if (corpo !== undefined) opzioni.body = JSON.stringify(corpo)

  const risposta = await fetch(endpoint, opzioni)
  const dati = await risposta.json()

  if (!risposta.ok) throw new Error(dati.errore || 'Errore del server')
  return dati as T
}

export interface ProdottoBackend {
  idProdotto: number
  nome: string
  descrizione: string
  prezzo: number
  disponibile: boolean
  categoria?: string
}

export interface RiderBackend {
  idRider: number
  nome: string
  stato: string
  posizione: string
  mezzoDiTrasporto: string
  numeroOrdiniAttivi: number
}

export interface OrdineCreato {
  idOrdine: number
  stato: string
  totale: number
  indirizzoConsegna: string
  prodotti: unknown[]
}

export interface ClienteCreato {
  idCliente: number
  nome: string
  telefono: string
  indirizzo: string
}

export const Auth = {
  registrati: (nome: string, email: string, password: string) =>
    chiama<{ messaggio: string; utente: UtenteInfo }>('/auth/registrati', 'POST', { nome, email, password }),

  login: (email: string, password: string) =>
    chiama<{ messaggio: string; token: string; utente: UtenteInfo }>('/auth/login', 'POST', { email, password }),

  profilo: () =>
    chiama<UtenteInfo>('/auth/profilo'),
}

export const Prodotti = {
  disponibili: () => chiama<ProdottoBackend[]>('/prodotti/disponibili'),
  tutti: () => chiama<ProdottoBackend[]>('/prodotti/'),
}

export const RiderAPI = {
  disponibili: () => chiama<RiderBackend[]>('/rider/disponibili'),
  tutti: () => chiama<RiderBackend[]>('/rider/'),
}

export const Ordini = {
  crea: (idCliente: number, indirizzoConsegna: string, prodotti: { idProdotto: number; quantita: number }[]) =>
    chiama<OrdineCreato>('/ordini/', 'POST', { idCliente, indirizzoConsegna, prodotti }),
}

export const Clienti = {
  crea: (nome: string, telefono: string, indirizzo: string) =>
    chiama<ClienteCreato>('/clienti/', 'POST', { nome, telefono, indirizzo }),
}