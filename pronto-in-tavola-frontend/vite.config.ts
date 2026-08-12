import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/auth':     { target: 'http://localhost:5000', changeOrigin: true },
      '/prodotti': { target: 'http://localhost:5000', changeOrigin: true },
      '/ordini':   { target: 'http://localhost:5000', changeOrigin: true },
      '/rider':    { target: 'http://localhost:5000', changeOrigin: true },
      '/clienti':  { target: 'http://localhost:5000', changeOrigin: true },
    }
  }
})