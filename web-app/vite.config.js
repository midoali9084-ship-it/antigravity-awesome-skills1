import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import process from 'node:process'

// https://vite.dev/config/
// BASE_PATH is set by the GitHub Pages workflow (e.g. "/repo-name/").
// Locally it defaults to "/" so `npm run dev` keeps working unchanged.
export default defineConfig({
  base: process.env.BASE_PATH || '/',
  plugins: [react()],
})
