import { useState, FormEvent } from 'react'
import { Link } from 'react-router-dom'

function FormLogin() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [rememberMe, setRememberMe] = useState(false)
  const [errore, setErrore] = useState('')

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!email || !password) {
      setErrore('Compila tutti i campi.')
      return
    }
    setErrore('')
    console.log('Login con:', email, password, 'Ricordami:', rememberMe)
  }

  return (
    <div className="w-full max-w-md bg-white rounded-2xl shadow-sm border border-gray-100 p-8">

      <h1 className="text-2xl font-bold text-gray-900 mb-1">Bentornato!</h1>
      <p className="text-sm text-gray-500 mb-8">Accedi al tuo account</p>

      {errore && (
        <div className="mb-6 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-4 py-3">
          {errore}
        </div>
      )}

      <form onSubmit={handleSubmit} className="flex flex-col gap-5">

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
          <div className="flex items-center justify-between">
            <label className="text-sm font-medium text-gray-700">Password</label>
            <a href="#" className="text-xs text-gray-400 hover:text-gray-700 transition-colors">
              Password dimenticata?
            </a>
          </div>
          <input
            type="password"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-gray-900 transition"
          />
        </div>

        <div className="flex items-center gap-3">
          <label className="inline-flex items-center text-sm text-gray-700">
            <input
              type="checkbox"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
              className="h-4 w-4 rounded border-gray-300 text-black focus:ring-black"
            />
            <span className="ml-2">Ricordami</span>
          </label>
        </div>

        <button
          type="submit"
          className="w-full bg-black text-white text-sm font-semibold py-3 rounded-lg hover:bg-gray-800 transition-colors duration-200 mt-2"
        >
          Accedi
        </button>

      </form>

      <p className="text-center text-sm text-gray-400 mt-6">
        Non hai un account?{' '}
        <Link to="/registrati" className="text-gray-900 font-medium hover:underline">
          Registrati
        </Link>
      </p>

    </div>
  )
}

export default FormLogin