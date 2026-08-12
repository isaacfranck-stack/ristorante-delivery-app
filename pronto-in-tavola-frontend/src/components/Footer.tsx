import { Link } from 'react-router-dom'

function Footer() {
  return (
    <footer className="w-full bg-stone-800 text-white mt-auto">
      <div className="max-w-6xl mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-3 gap-10">

        {/* Sinistra — Social */}
        <div className="flex flex-col gap-4">
          <p className="text-white font-semibold text-base">Seguici</p>
          <div className="flex gap-4">
            {/* Facebook */}
            <a href="https://facebook.com" target="_blank" rel="noreferrer"
              className="w-9 h-9 rounded-full border border-white/20 flex items-center justify-center hover:border-white transition-colors duration-200">
              <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4 fill-white" viewBox="0 0 24 24">
                <path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>
              </svg>
            </a>
            {/* Instagram */}
            <a href="https://instagram.com" target="_blank" rel="noreferrer"
              className="w-9 h-9 rounded-full border border-white/20 flex items-center justify-center hover:border-white transition-colors duration-200">
              <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4 stroke-white fill-none" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" viewBox="0 0 24 24">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
                <circle cx="12" cy="12" r="4"/>
                <circle cx="17.5" cy="6.5" r="0.5" fill="white"/>
              </svg>
            </a>
            {/* WhatsApp */}
            <a href="https://wa.me/393476543210" target="_blank" rel="noreferrer"
              className="w-9 h-9 rounded-full border border-white/20 flex items-center justify-center hover:border-white transition-colors duration-200">
              <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4 fill-white" viewBox="0 0 24 24">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/>
                <path d="M12 0C5.373 0 0 5.373 0 12c0 2.123.554 4.116 1.523 5.847L.057 23.428a.75.75 0 0 0 .921.921l5.562-1.461A11.945 11.945 0 0 0 12 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-1.891 0-3.667-.523-5.183-1.433l-.371-.22-3.844 1.01 1.012-3.73-.242-.385A9.937 9.937 0 0 1 2 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/>
              </svg>
            </a>
          </div>
        </div>

        {/* Centro — Indirizzo e orari */}
        <div className="flex flex-col gap-2 text-sm text-gray-300">
          <p className="text-white font-semibold text-base mb-1">Dove siamo</p>
          <p>Via Po, 42 — Torino, 10123</p>
          <p>+39 347 654 3210</p>
          <div className="mt-3">
            <p className="text-white font-semibold mb-1">Orari</p>
            <p>Lun: <span className="text-gray-400">Chiuso</span></p>
            <p>Mar–Dom:</p>
            <p className="text-gray-400">12:00 – 15:00</p>
            <p className="text-gray-400">18:30 – 22:00</p>
          </div>
        </div>

        {/* Destra — Legale */}
        <div className="flex flex-col gap-2 text-sm text-gray-300">
          <p className="text-white font-semibold text-base mb-1">Informazioni legali</p>
          <p>P.IVA: 12345678901</p>
          <Link to="/privacy" className="hover:text-white transition-colors duration-200">
            Privacy Policy
          </Link>
          <Link to="/cookie" className="hover:text-white transition-colors duration-200">
            Cookie Policy
          </Link>
        </div>

      </div>

      {/* Barra inferiore */}
      <div className="border-t border-white/10 text-center py-4 text-xs text-gray-500">
        © {new Date().getFullYear()} MFI — Tutti i diritti riservati
      </div>
    </footer>
  )
}

export default Footer