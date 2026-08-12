import { useState, useEffect } from 'react'
import { useCarrello } from '../context/CarrelloContext'
import { Prodotti, type ProdottoBackend } from '../services/api'

function categoriaFallback(nome: string): string {
  const n = nome.toLowerCase()
  if (n.includes('acqua') || n.includes('birra') || n.includes('vino') || n.includes('heineken')) return 'bevande'
  if (n.includes('tiramisù') || n.includes('torta') || n.includes('cantucci')) return 'dolci'
  if (n.includes('spezzatino') || n.includes('cotechino') || n.includes('pollo') ||
      n.includes('baccalà') || n.includes('trippa') || n.includes('salsicce')) return 'secondi'
  return 'primi'
}

const tab = [
  { id: 'primi', label: 'I Nostri Primi' },
  { id: 'secondi', label: 'I Nostri Secondi' },
  { id: 'dolci', label: 'Dolci della Casa' },
  { id: 'bevande', label: 'Bevande' },
]

function Menu() {
  const { aggiungi, carrello } = useCarrello()
  const [sezioneAttiva, setSezioneAttiva] = useState('primi')
  const [prodotti, setProdotti] = useState<ProdottoBackend[]>([])
  const [caricamento, setCaricamento] = useState(true)
  const [errore, setErrore] = useState('')

  useEffect(() => {
    Prodotti.disponibili()
      .then(setProdotti)
      .catch(() => setErrore('Impossibile caricare il menu. Assicurati che il server sia avviato.'))
      .finally(() => setCaricamento(false))
  }, [])

  const prodottiSezione = prodotti.filter((p) => {
    const cat = p.categoria ?? categoriaFallback(p.nome)
    return cat === sezioneAttiva
  })

  return (
    <div className="max-w-2xl mx-auto px-4 py-12">

      <h1 className="text-3xl font-bold text-gray-900 mb-2">Il Nostro Menu</h1>
      <p className="text-sm text-gray-500 mb-8">
        Tutti i piatti sono preparati al momento con ingredienti freschi e di stagione.
      </p>

      <div className="flex flex-wrap gap-2 mb-8">
        {tab.map((t) => (
          <button
            key={t.id}
            onClick={() => setSezioneAttiva(t.id)}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors duration-200
              ${sezioneAttiva === t.id
                ? 'bg-black text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {caricamento && (
        <p className="text-sm text-gray-400 text-center py-8">Caricamento menu...</p>
      )}
      {errore && (
        <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-3 mb-6">
          {errore}
        </div>
      )}

      {!caricamento && !errore && (
        <div className="flex flex-col divide-y divide-gray-100">
          {prodottiSezione.length === 0 ? (
            <p className="text-sm text-gray-400 text-center py-8">Nessun piatto disponibile.</p>
          ) : (
            prodottiSezione.map((piatto) => {
              const prezzoFormattato = `€${piatto.prezzo.toFixed(2).replace('.', ',')}`
              const itemCarrello = carrello.find((p) => p.nome === piatto.nome)
              return (
                <div key={piatto.idProdotto} className="flex items-center justify-between gap-4 py-4">
                  <div className="flex flex-col gap-0.5 flex-1">
                    <span className="text-base font-semibold text-gray-900">{piatto.nome}</span>
                    {piatto.descrizione && (
                      <span className="text-sm text-gray-500">{piatto.descrizione}</span>
                    )}
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-base font-semibond text-gray-900 whitespace-nowrap">
                      {prezzoFormattato}
                    </span>
                    {itemCarrello && (
                      <span className="w-7 text-center text-base font-semibold text-black select-none">
                        x{itemCarrello.quantita}
                      </span>
                    )}
                    <button
                      onClick={() => aggiungi({ nome: piatto.nome, prezzo: prezzoFormattato, idProdotto: piatto.idProdotto })}
                      className="w-8 h-8 rounded-full bg-black text-white flex items-center justify-center text-lg hover:bg-gray-800 transition-colors duration-200"
                    >
                      +
                    </button>
                  </div>
                </div>
              )
            })
          )}
        </div>
      )}

      <p className="text-xs text-gray-400 mt-10 text-center">
        Confezionamento termico per mantenere la temperatura ottimale durante il trasporto. Buon appetito! 🍷
      </p>

    </div>
  )
}

export default Menu