const { defineConfig } = require('cypress');
const getCompareSnapshotsPlugin = require('cypress-visual-regression/dist/plugin');

module.exports = defineConfig({
  video: false,
  screenshotOnRunFailure: true,
  fixturesFolder: 'test/cypress/fixtures',
  videosFolder: 'test/cypress/videos',
  screenshotsFolder: 'test/cypress/screenshots',
  defaultCommandTimeout: 25000,
  blockHosts: ['*google-analytics.com', '*googletagmanager.com'],
  e2e: {
    baseUrl: 'http://localhost:8000',
    specPattern: 'test/cypress/integration/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'test/cypress/support/e2e.js',
    excludeSpecPattern: 'test/cypress/integration/**/*-helpers.cy.js',
    setupNodeEvents(on, config) {
      getCompareSnapshotsPlugin(on, config);
    },
  },
  component: {
    specPattern: 'test/cypress/component/**/*.cy.{js,jsx,ts,tsx}',
    excludeSpecPattern: 'test/cypress/component/**/*-helpers.cy.js',
  },
  env: {
    ENVIRONMENT: 'local-machine',
    SNAPSHOT_BASE_DIRECTORY: `test/cypress/visual-regression/base`,
    SNAPSHOT_DIFF_DIRECTORY: `test/cypress/visual-regression/diff`,
    type: 'actual',
  },
});
