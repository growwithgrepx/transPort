const { defineConfig } = require('cypress');

module.exports = defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000', // Adjust if your dev server runs on a different port
    specPattern: 'cypress/e2e/**/*.cy.{js,ts,jsx,tsx}',
  },
}); 