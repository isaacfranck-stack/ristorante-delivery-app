import { Clienti, Ordini, leggiUtente } from './api'

export type Ordine = {
  indirizzo: string
  pagamento: 'carta' | 'contanti'
  piatti: { nome: string; prezzo: string; quantita: number; idProdotto?: number }[]
}

export type RispostaOrdine = {
  successo: boolean
  idOrdine?: string
  messaggio?: string
}

export async function inviaOrdine(ordine: Ordine): Promise<RispostaOrdine> {
  try {
    let idCliente: number

    const utente = leggiUtente()
    if (utente) {
      idCliente = utente.id
    } else {
      const cliente = await Clienti.crea('Cliente Guest', '', ordine.indirizzo)
      idCliente = cliente.idCliente
    }

    const prodottiBackend = ordine.piatti.map((p) => ({
      idProdotto: p.idProdotto!,
      quantita: p.quantita,
    }))

    const risposta = await Ordini.crea(idCliente, ordine.indirizzo, prodottiBackend)

    return {
      successo: true,
      idOrdine: `ORD-${risposta.idOrdine}`,
      messaggio: 'Ordine ricevuto con successo',
    }
  } catch (err: unknown) {
    const msg = err instanceof Error ? err.message : 'Errore sconosciuto'
    return { successo: false, messaggio: msg }
  }
}