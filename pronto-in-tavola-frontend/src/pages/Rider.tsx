import { useEffect, useState } from 'react'
import { getAllRiders, getRider, type Rider } from '../services/riderService'

function Rider() {
  const [riders, setRiders] = useState<Rider[]>([])
  const [migliore, setMigliore] = useState<Rider | null>(null)
  const [caricamento, setCaricamento] = useState(true)

  useEffect(() => {
    setRiders(getAllRiders())

    getRider()
      .then((r) => setMigliore(r))
      .catch(() => setMigliore(null))
      .finally(() => setCaricamento(false))
  }, [])

  return (
    <div className="max-w-2xl mx-auto px-4 py-12 flex flex-col gap-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">I nostri rider</h1>
        <p className="text-sm text-gray-500 mt-1">
          Il sistema seleziona automaticamente il rider più vicino e disponibile per ogni ordine.
        </p>
      </div>

      {/* Banner rider selezionato */}
      {caricamento ? (
        <div className="bg-gray-50 border border-gray-200 rounded-2xl p-5 flex items-center gap-3 animate-pulse">
          <div className="w-10 h-10 rounded-full bg-gray-200" />
          <div className="flex flex-col gap-2 flex-1">
            <div className="h-3 bg-gray-200 rounded w-1/3" />
            <div className="h-3 bg-gray-200 rounded w-1/2" />
          </div>
        </div>
      ) : migliore ? (
        <div className="bg-black text-white rounded-2xl p-5 flex items-center gap-4 shadow-md">
          <img
            src={migliore.foto}
            alt={migliore.nome}
            onError={(e) => { e.currentTarget.style.display = 'none' }}
            className="w-12 h-12 rounded-full object-cover bg-gray-700 flex-shrink-0"
          />
          <div className="flex-1 min-w-0">
            <p className="text-xs font-medium text-gray-400 uppercase tracking-widest mb-0.5">
              Selezionato per il prossimo ordine
            </p>
            <p className="text-base font-semibold truncate">{migliore.nome}</p>
            <p className="text-sm text-gray-400">
              ⭐ {migliore.voto} · {migliore.km} km · {migliore.tempo}
            </p>
          </div>
          <span className="text-2xl flex-shrink-0">🏍️</span>
        </div>
      ) : (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-5 text-sm text-red-600">
          Nessun rider disponibile al momento.
        </div>
      )}

      {/* Cards rider */}
      <div className="flex flex-col gap-3">
        {riders.map((rider) => {
          const isSelected = migliore?.id === rider.id

          return (
            <div
              key={rider.id}
              className={`bg-white border rounded-2xl p-5 shadow-sm flex items-center gap-4 transition-all duration-200
                ${isSelected
                  ? 'border-black ring-1 ring-black'
                  : rider.disponibile
                    ? 'border-gray-100 hover:border-gray-300'
                    : 'border-gray-100 opacity-50'
                }`}
            >
              {/* Avatar */}
              <div className="relative flex-shrink-0">
                <img
                  src={rider.foto}
                  alt={rider.nome}
                  onError={(e) => { e.currentTarget.style.display = 'none' }}
                  className="w-14 h-14 rounded-full object-cover bg-gray-100"
                />
                {/* Badge disponibilità */}
                <span
                  className={`absolute bottom-0 right-0 w-3.5 h-3.5 rounded-full border-2 border-white
                    ${rider.disponibile ? 'bg-green-400' : 'bg-gray-300'}`}
                />
              </div>

              {/* Info */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-sm font-semibold text-gray-900 truncate">{rider.nome}</span>
                  {isSelected && (
                    <span className="text-[10px] font-semibold bg-black text-white px-2 py-0.5 rounded-full uppercase tracking-wide">
                      Selezionato
                    </span>
                  )}
                  {!rider.disponibile && (
                    <span className="text-[10px] font-medium bg-gray-100 text-gray-400 px-2 py-0.5 rounded-full">
                      Non disponibile
                    </span>
                  )}
                </div>
                <p className="text-xs text-gray-400 mt-0.5">Targa: {rider.targa}</p>
                <div className="flex flex-wrap gap-x-4 gap-y-0.5 mt-1.5">
                  <span className="text-xs text-gray-500">⭐ {rider.voto}</span>
                  <span className="text-xs text-gray-500">📍 {rider.km} km</span>
                  <span className="text-xs text-gray-500">🕐 {rider.tempo}</span>
                  <span className="text-xs text-gray-500">📦 {rider.consegneOggi} consegne oggi</span>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      <p className="text-xs text-gray-400 text-center">
        I rider vengono assegnati automaticamente in base alla distanza e alla disponibilità.
      </p>
    </div>
  )
}

export default Rider