import { createContext, useContext, useState } from 'react'

export type Piatto = {
  nome: string
  prezzo: string
  quantita: number
  idProdotto?: number
}

type CarrelloContextType = {
  carrello: Piatto[]
  aggiungi: (piatto: { nome: string; prezzo: string; idProdotto?: number }) => void
  rimuovi: (nome: string) => void
  svuota: () => void
}

const CarrelloContext = createContext<CarrelloContextType | null>(null)

export function CarrelloProvider({ children }: { children: React.ReactNode }) {
  const [carrello, setCarrello] = useState<Piatto[]>([])

  const aggiungi = (piatto: { nome: string; prezzo: string; idProdotto?: number }) => {
    setCarrello((prev) => {
      const esistente = prev.find((p) => p.nome === piatto.nome)
      if (esistente) {
        return prev.map((p) =>
          p.nome === piatto.nome ? { ...p, quantita: p.quantita + 1 } : p
        )
      }
      return [...prev, { ...piatto, quantita: 1 }]
    })
  }

  const rimuovi = (nome: string) => {
    setCarrello((prev) => prev.filter((p) => p.nome !== nome))
  }

  const svuota = () => setCarrello([])

  return (
    <CarrelloContext.Provider value={{ carrello, aggiungi, rimuovi, svuota }}>
      {children}
    </CarrelloContext.Provider>
  )
}

export function useCarrello() {
  const context = useContext(CarrelloContext)
  if (!context) throw new Error('useCarrello deve essere usato dentro CarrelloProvider')
 return context!
}