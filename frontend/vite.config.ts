import { defineConfig } from 'vitest/config'

export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
      },
    },
  },
  test: {
    environment: 'jsdom',
    include: ['./tests/scenarios.test.ts'],
    setupFiles: ['./tests/setup.ts'],
    restoreMocks: true,
  },
})
