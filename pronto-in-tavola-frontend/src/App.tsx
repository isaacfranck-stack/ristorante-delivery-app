import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Home from './pages/Home'
import Menu from './pages/Menu'
import Login from './pages/Login'
import Carrello from './pages/Carrello'
import Rider from './pages/Rider'
import Cookie from './pages/Cookie'
import Privacy from './pages/Privacy'
import Registrazione from './pages/Registrazione'
import { CarrelloProvider } from './context/CarrelloContext'


function App() {
  return (
    <BrowserRouter>
      <CarrelloProvider>
        <div className="min-h-screen flex flex-col">
          <Navbar />
          <main className="flex-1">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/menu" element={<Menu />} />
              <Route path="/login" element={<Login />} />
              <Route path="/carrello" element={<Carrello />} />
              <Route path="/rider" element={<Rider />} />
              <Route path="/cookie" element={<Cookie />} />
              <Route path="/privacy" element={<Privacy />} />
              <Route path="/registrati" element={<Registrazione />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </CarrelloProvider>
    </BrowserRouter>
  )
}

export default App