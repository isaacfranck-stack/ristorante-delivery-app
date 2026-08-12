import { RiderAPI, type RiderBackend } from './api'

export type Rider = {
  id: string
  nome: string
  foto: string
  voto: number
  targa: string
  tempo: string
  disponibile: boolean
  consegneOggi: number
  km: number
}

function adattaRider(r: RiderBackend): Rider {
  return {
    id:           String(r.idRider),
    nome:         r.nome,
    foto:         `https://api.dicebear.com/7.x/thumbs/svg?seed=${encodeURIComponent(r.nome)}`,
    voto:         4.5 + Math.random() * 0.5,
    targa:        r.mezzoDiTrasporto || 'N/D',
    tempo:        '20–30 min',
    disponibile:  r.stato === 'disponibile',
    consegneOggi: r.numeroOrdiniAttivi,
    km:           Math.round((0.5 + Math.random() * 3) * 10) / 10,
  }
}

export function getAllRiders(): Rider[] {
  return []
}

export async function getRider(): Promise<Rider> {
  const riderBackend = await RiderAPI.disponibili()

  if (riderBackend.length === 0) {
    throw new Error('Nessun rider disponibile al momento')
  }

  const riders = riderBackend.map(adattaRider)
  return riders.sort((a, b) => a.consegneOggi - b.consegneOggi)[0]
}