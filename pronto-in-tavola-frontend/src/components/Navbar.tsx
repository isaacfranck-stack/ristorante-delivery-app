import { useState } from 'react'
import { NavLink } from 'react-router-dom'

function Navbar() {
  const [menuAperto, setMenuAperto] = useState(false)

  const baseLink = "text-lg font-medium text-gray-600 hover:text-black transition-colors duration-200"
  const activeLink = "text-black font-semibold border-b-2 border-black"

  const links = [
    { to: "/", label: "Home" },
    { to: "/menu", label: "Menu" },
    { to: "/rider", label: "I nostri rider" },
  ]

  return (
    <nav className="w-full bg-white shadow-sm border-b border-gray-200">

      {/* Barra principale */}
      <div className="flex items-center justify-between px-6 py-4">

        {/* Logo */}
        <NavLink to="/" onClick={() => setMenuAperto(false)}>
          <img src="/logo.png" alt="Logo" className="h-25 w-auto" />
        </NavLink> 

        {/* Links desktop */}
        <ul className="hidden md:flex items-center gap-8">
          {links.map(({ to, label }) => (
            <li key={to}>
              <NavLink
                to={to}
                end
                className={({ isActive }) =>
                  `${baseLink} ${isActive ? activeLink : ""}`
                }
              >
                {label}
              </NavLink>
            </li>
          ))}
        </ul>

        {/* Azioni desktop */}
        <div className="hidden md:flex items-center gap-3">
          <NavLink
            to="/carrello"
            className={({ isActive }) =>
              `text-lg font-medium px-5 py-2 rounded-full border transition-colors duration-200
              ${isActive ? "bg-black text-white border-black" : "border-gray-300 text-gray-700 hover:border-black hover:text-black"}`
            }
          >
            🛒 Carrello
          </NavLink>
          <NavLink
            to="/login"
            className={({ isActive }) =>
              `text-lg font-medium px-5 py-2 rounded-full transition-colors duration-200
              ${isActive ? "bg-orange-900 text-white" : "bg-black text-white hover:bg-gray-800"}`
            }
          >
            Accedi
          </NavLink>
        </div>

        {/* Hamburger mobile */}
        <button
          className="md:hidden flex flex-col gap-1.5 p-2"
          onClick={() => setMenuAperto(!menuAperto)}
          aria-label="Apri menu"
        >
          <span className={`block w-6 h-0.5 bg-black transition-all duration-300 ${menuAperto ? "rotate-45 translate-y-2" : ""}`} />
          <span className={`block w-6 h-0.5 bg-black transition-all duration-300 ${menuAperto ? "opacity-0" : ""}`} />
          <span className={`block w-6 h-0.5 bg-black transition-all duration-300 ${menuAperto ? "-rotate-45 -translate-y-2" : ""}`} />
        </button>

      </div>

      {/* Menu mobile a tendina */}
      {menuAperto && (
        <div className="md:hidden flex flex-col gap-4 px-6 pb-6 border-t border-gray-100">
          {links.map(({ to, label }) => (
            <NavLink
              key={to}
              to={to}
              end
              onClick={() => setMenuAperto(false)}
              className={({ isActive }) =>
                `text-lg font-medium py-1 ${isActive ? "text-black font-semibold" : "text-gray-600"}`
              }
            >
              {label}
            </NavLink>
          ))}
          <div className="flex flex-col gap-3 pt-2">
            <NavLink
              to="/carrello"
              onClick={() => setMenuAperto(false)}
              className="text-lg font-medium text-center px-5 py-2 rounded-full border border-gray-300 text-gray-700"
            >
              🛒 Carrello
            </NavLink>
            <NavLink
              to="/login"
              onClick={() => setMenuAperto(false)}
              className="text-lg font-medium text-center px-5 py-2 rounded-full bg-black text-white"
            >
              Accedi
            </NavLink>
          </div>
        </div>
      )}

    </nav>
  )
}

export default Navbar