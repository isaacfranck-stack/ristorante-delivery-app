import { Link } from 'react-router-dom'

function Home() {
  return (
    <main className="w-full">
      {/* Hero Section */}
      <section 
        className="relative w-full h-125 bg-cover bg-center flex items-center justify-center"
        style={{
          backgroundImage: 'linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url(../public/home-background.png)',
          backgroundPosition: 'center'
        }}
      >
        <div className="text-center text-white px-4">
          <p className="text-sm mb-2 font-light tracking-widest">OSTERIA DA ASPORTO</p>
          <h1 className="font-extrabold text-9xl md:text-7xl mb-4 italic">
            Pronto in Tavola
          </h1>
          <p className="text-base md:text-lg mb-8 max-w-2xl mx-auto font-light">
            Il profumo della nostra cucina, direttamente alla tua porta.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Link 
              to="/menu"
              className="bg-black hover:bg-gray-800 text-white px-6 py-2 rounded-full font-medium text-sm transition-colors duration-200"
            >
              Scopri i nostri piatti
            </Link>
            <button className="border border-white text-white px-6 py-2 rounded-full font-medium text-sm hover:bg-white hover:text-black transition-colors duration-200">
              Chiama ora
            </button>
          </div>
        </div>
      </section>

      {/* Chi siamo Section */}
      <section className="py-16 md:py-24 px-4 md:px-8 lg:px-16">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
            {/* Testo */}
            <div>
              <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
                Chi siamo
              </h2>
              <p className="text-base text-gray-700 mb-4 leading-relaxed">
                Siamo un'osteria da asporto con la passione per la cucina tradizionale, proprio come quella della nonna. I nostri piatti sono creati con ricette autentiche e ingredienti freschi e di qualità, per offrirti un'esperienza culinaria genuina direttamente a casa tua.
              </p>
              <p className="text-base text-gray-700 leading-relaxed">
                Crediamo nel sapore autentico, negli ingredienti locali e nella semplicità. La famiglia è la cosa più importante per noi, e questo amore si riflette in tutto quello che prepariamo per te.
              </p>
            </div>

            {/* Immagine */}
            <div className="flex justify-center">
              <img 
                src="../public/carbonara.png"
                alt="Piatti della nostra cucina"
                className="w-full max-w-sm object-cover rounded"
              />
            </div>
          </div>
        </div>
      </section>
    </main>
  )
}

export default Home