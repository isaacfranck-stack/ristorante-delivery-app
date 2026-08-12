import { useState } from 'react'
import { Link } from 'react-router-dom'

function FormRegistrazione() {
  const [nome, setNome] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confermaPassword, setConfermaPassword] = useState('')
  const [errore, setErrore] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!nome || !email || !password || !confermaPassword) {
      setErrore('Compila tutti i campi.')
      return
    }
    if (password !== confermaPassword) {
      setErrore('Le password non coincidono.')
      return
    }
    setErrore('')
    console.log('Registrazione con:', nome, email, password)
  }

  return (
    <div className="w-full max-w-md bg-white rounded-2xl shadow-sm border border-gray-100 p-8">

      <h1 className="text-2xl font-bold text-gray-900 mb-1">Crea un account</h1>
      <p className="text-sm text-gray-500 mb-8">Registrati per ordinare</p>

      {errore && (
        <div className="mb-6 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-3">
          {errore}
        </div>
      )}

      <form onSubmit={handleSubmit} className="flex flex-col gap-5">

        <div className="flex flex-col gap-1.5">
          <label className="text-sm font-medium text-gray-700">Nome e cognome</label>
          <input
            type="text"
            placeholder="Mario Rossi"
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            className="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900 transition"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-sm font-medium text-gray-700">Email</label>
          <input
            type="email"
            placeholder="nome@email.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900 transition"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900 transition"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label className="text-sm font-medium text-gray-700">Conferma password</label>
          <input
            type="password"
            placeholder="••••••••"
            value={confermaPassword}
            onChange={(e) => setConfermaPassword(e.target.value)}
            className="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900 transition"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-black text-white text-sm font-semibold py-3 rounded-lg hover:bg-gray-800 transition-colors duration-200 mt-2"
        >
          Registrati
        </button>

      </form>

      <p className="text-center text-sm text-gray-400 mt-6">
        Hai già un account?{' '}
        <Link to="/login" className="text-gray-900 font-medium hover:underline">
          Accedi
        </Link>
      </p>

    </div>
  )
}

export default FormRegistrazione