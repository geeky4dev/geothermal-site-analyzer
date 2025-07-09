import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Detectamos si estamos en desarrollo
const isDev = process.env.NODE_ENV === 'development'

export default defineConfig({
  plugins: [react()],
  server: isDev
    ? {
        proxy: {
          // Proxy para todas las peticiones que empiecen con /api
          '/api': {
            target: 'http://localhost:5001',
            changeOrigin: true,
            secure: false,
          },
        },
      }
    : undefined, // En producción no se usa proxy
})

