const { defineConfig } = require('cypress')

module.exports = defineConfig({
  video: false,
  screenshotOnRunFailure: false,
  fixturesFolder: 'test/cypress/fixtures',
  videosFolder: 'test/cypress/videos',
  screenshotsFolder: 'test/cypress/screenshots',
  defaultCommandTimeout: 25000,
  blockHosts: [
    '*google-analytics.com',
    '*googletagmanager.com'
  ],
  e2e: {
    baseUrl: 'http://localhost:8000',
    specPattern: 'test/cypress/integration/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'test/cypress/support/e2e.js',
    excludeSpecPattern: 'test/cypress/integration/**/*-helpers.cy.js',
  },
  component: {
    specPattern: 'test/cypress/component/**/*.cy.{js,jsx,ts,tsx}',
    excludeSpecPattern: 'test/cypress/component/**/*-helpers.cy.js',
  },
})
