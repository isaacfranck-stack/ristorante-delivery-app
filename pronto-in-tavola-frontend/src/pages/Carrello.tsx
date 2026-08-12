import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useCarrello } from '../context/CarrelloContext'
import { getRider, type Rider } from '../services/riderService'
import { inviaOrdine } from '../services/ordineService'

function Carrello() {
  const { carrello, rimuovi, svuota } = useCarrello()
  const [indirizzo, setIndirizzo] = useState('')
  const [pagamento, setPagamento] = useState<'carta' | 'contanti'>('carta')
  const [numeroCarta, setNumeroCarta] = useState('')
  const [errore, setErrore] = useState('')
  const [caricamento, setCaricamento] = useState(false)
  const [ordinato, setOrdinato] = useState(false)
  const [rider, setRider] = useState<Rider | null>(null)
  const [idOrdine, setIdOrdine] = useState<string | null>(null)

  const totale = carrello.reduce((acc, p) => {
    const prezzo = parseFloat(p.prezzo.replace('€', '').replace(',', '.'))
    return acc + prezzo * p.quantita
  }, 0)

  const handleOrdine = async () => {
    if (carrello.length === 0) {
      setErrore('Il carrello è vuoto.')
      return
    }
    if (!indirizzo) {
      setErrore('Inserisci un indirizzo di consegna.')
      return
    }
    if (pagamento === 'carta' && !numeroCarta) {
      setErrore('Inserisci il numero di carta.')
      return
    }

    setErrore('')
    setCaricamento(true)

    try {
      const [riderTrovato, risposta] = await Promise.all([
        getRider(),
        inviaOrdine({ indirizzo, pagamento, piatti: carrello })
      ])

      if (risposta.successo) {
        setRider(riderTrovato)
        setIdOrdine(risposta.idOrdine ?? null)
        setOrdinato(true)
        svuota()
      } else {
        setErrore(risposta.messaggio ?? 'Qualcosa è andato storto. Riprova.')
      }
    } catch {
      setErrore('Errore di connessione. Riprova.')
    } finally {
      setCaricamento(false)
    }
  }

  // --- SCHERMATA POST ORDINE ---
  if (ordinato && rider) {
    return (
      <div className="max-w-2xl mx-auto px-4 py-12 flex flex-col gap-6">

        {/* Conferma */}
        <div className="bg-green-50 border border-green-200 rounded-2xl p-6 text-center">
          <p className="text-3xl mb-2">✅</p>
          <h2 className="text-xl font-bold text-green-800 mb-1">Ordine confermato!</h2>
          {idOrdine && (
            <p className="text-xs text-green-600 mt-1">Numero ordine: {idOrdine}</p>
          )}
          <p className="text-sm text-green-600 mt-1">Il tuo ordine è in preparazione.</p>
        </div>

        {/* Rider */}
        <div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm flex flex-col gap-4">
          <h3 className="text-base font-semibold text-gray-900">Il tuo rider</h3>
          <div className="flex items-center gap-4">
            <img
              src={rider.foto}
              alt={rider.nome}
              onError={(e) => {
                e.currentTarget.style.display = 'none'
              }}
              className="w-14 h-14 rounded-full object-cover bg-gray-100"
            />
            <div>
              <p className="font-semibold text-gray-900">{rider.nome}</p>
              <p className="text-sm text-gray-500">⭐ {rider.voto} · Targa: {rider.targa}</p>
            </div>
          </div>
        </div>

        {/* Tempo */}
        <div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm">
          <h3 className="text-base font-semibold text-gray-900 mb-1">Tempo stimato</h3>
          <p className="text-3xl font-bold text-gray-900">{rider.tempo}</p>
          <p className="text-sm text-gray-500 mt-1">Consegna a: {indirizzo}</p>
        </div>

        {/* Stato ordine */}
        <div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm flex flex-col gap-4">
          <h3 className="text-base font-semibold text-gray-900">Stato ordine</h3>
          {[
            { label: 'Ordine ricevuto', fatto: true },
            { label: 'In preparazione', fatto: true },
            { label: 'In consegna', fatto: false },
            { label: 'Consegnato', fatto: false },
          ].map((step) => (
            <div key={step.label} className="flex items-center gap-3">
              <div className={`w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold
                ${step.fatto ? 'bg-black text-white' : 'bg-gray-100 text-gray-400'}`}>
                {step.fatto ? '✓' : ''}
              </div>
              <span className={`text-sm ${step.fatto ? 'text-gray-900 font-medium' : 'text-gray-400'}`}>
                {step.label}
              </span>
            </div>
          ))}
        </div>

        <Link
          to="/menu"
          className="w-full text-center py-3 rounded-lg border border-gray-200 text-sm font-medium text-gray-600 hover:bg-gray-50 transition-colors"
        >
          Torna al menu
        </Link>

      </div>
    )
  }

  // --- SCHERMATA CARRELLO ---
  return (
    <div className="max-w-2xl mx-auto px-4 py-12 flex flex-col gap-6">

      <h1 className="text-3xl font-bold text-gray-900">Il tuo carrello</h1>

      {carrello.length === 0 ? (
        <div className="text-center py-16 flex flex-col gap-4">
          <p className="text-gray-400 text-sm">Non hai ancora aggiunto nulla.</p>
          <Link
            to="/menu"
            className="mx-auto px-6 py-2.5 rounded-full bg-black text-white text-sm font-medium hover:bg-gray-800 transition-colors"
          >
            Vai al menu
          </Link>
        </div>
      ) : (
        <>
          {/* Riepilogo */}
          <div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm">
            <h2 className="text-base font-semibold text-gray-900 mb-4">Riepilogo ordine</h2>
            <div className="flex flex-col divide-y divide-gray-100">
              {carrello.map((p) => (
                <div key={p.nome} className="flex items-center justify-between py-3 gap-4">
                  <div className="flex flex-col flex-1">
                    <span className="text-sm font-medium text-gray-900">{p.nome}</span>
                    <span className="text-xs text-gray-400">x{p.quantita}</span>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="text-sm font-semibold text-gray-900">{p.prezzo}</span>
                    <button
                      onClick={() => rimuovi(p.nome)}
                      className="text-xs text-red-400 hover:text-red-600 transition-colors"
                    >
                      Rimuovi
                    </button>
                  </div>
                </div>
              ))}
            </div>
            <div className="flex justify-between items-center pt-4 border-t border-gray-100 mt-2">
              <span className="text-base font-bold text-gray-900">Totale</span>
              <span className="text-base font-bold text-gray-900">
                €{totale.toFixed(2).replace('.', ',')}
              </span>
            </div>
          </div>

          {/* Indirizzo */}
          <div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm flex flex-col gap-3">
            <h2 className="text-base font-semibold text-gray-900">Indirizzo di consegna</h2>
            <input
              type="text"
              placeholder="Via Roma, 1 - Torino"
              value={indirizzo}
              onChange={(e) => setIndirizzo(e.target.value)}
              className="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900 transition"
            />
          </div>

          {/* Pagamento */}
          <div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm flex flex-col gap-4">
            <h2 className="text-base font-semibold text-gray-900">Metodo di pagamento</h2>
            <div className="flex gap-3">
              <button
                onClick={() => setPagamento('carta')}
                className={`flex-1 py-2.5 rounded-lg border text-sm font-medium transition-colors
                  ${pagamento === 'carta'
                    ? 'bg-black text-white border-black'
                    : 'border-gray-200 text-gray-600 hover:border-gray-400'}`}
              >
                💳 Carta
              </button>
              <button
                onClick={() => setPagamento('contanti')}
                className={`flex-1 py-2.5 rounded-lg border text-sm font-medium transition-colors
                  ${pagamento === 'contanti'
                    ? 'bg-black text-white border-black'
                    : 'border-gray-200 text-gray-600 hover:border-gray-400'}`}
              >
                💵 Contanti
              </button>
            </div>
            {pagamento === 'carta' && (
              <input
                type="text"
                placeholder="Numero carta"
                value={numeroCarta}
                onChange={(e) => setNumeroCarta(e.target.value)}
                className="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900 transition"
              />
            )}
            {pagamento === 'contanti' && (
              <p className="text-sm text-gray-400">Pagherai in contanti al momento della consegna.</p>
            )}
          </div>

          {/* Errore */}
          {errore && (
            <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-3">
              {errore}
            </div>
          )}

          {/* Bottone conferma */}
          <button
            onClick={handleOrdine}
            disabled={caricamento}
            className="w-full bg-black text-white font-semibold py-3 rounded-lg hover:bg-gray-800 transition-colors duration-200 disabled:opacity-50"
          >
            {caricamento ? 'Invio ordine...' : `Conferma ordine — €${totale.toFixed(2).replace('.', ',')}`}
          </button>
        </>
      )}
    </div>
  )
}

export default Carrello