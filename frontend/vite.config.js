import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import Inspect from 'vite-plugin-inspect'

export default defineConfig(({ command }) => ({
  // command === '/' for 'serve', '/static/' for build.
  base: command === 'serve' ? '/' : '/static/',
  plugins: [
    vue(),
    vueDevTools(),
    Inspect(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      '/api': 'http://127.0.0.1:5000',
    },
    // Optionally, if you need a more granular SPA fallback configuration, you can also plug in connect-history-api-fallback here
  },
}))
