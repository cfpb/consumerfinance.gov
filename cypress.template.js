import { defineConfig } from 'cypress';
import cypressFailFast from 'cypress-fail-fast/plugin';

export default defineConfig({
  allowCypressEnv: false,
  experimentalMemoryManagement: true,
  screenshotOnRunFailure: true,
  fixturesFolder: 'test/cypress/fixtures',
  videosFolder: 'test/cypress/videos',
  screenshotsFolder: 'test/cypress/screenshots',
  defaultCommandTimeout: 25000,
  blockHosts: [
    '*.federalregister.gov',
    '*.geo.census.gov',
    '*google-analytics.com',
    '*googletagmanager.com',
    '*.newrelic.com',
    '*.nr-data.net',
  ],
  e2e: {
    baseUrl: 'http://localhost:8000',
    specPattern: 'test/cypress/integration/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'test/cypress/support/e2e.js',
    excludeSpecPattern: 'test/cypress/integration/**/*-helpers.cy.js',
    setupNodeEvents(on, config) {
      cypressFailFast(on, config);
    },
  },
  component: {
    specPattern: 'test/cypress/component/**/*.cy.{js,jsx,ts,tsx}',
    excludeSpecPattern: 'test/cypress/component/**/*-helpers.cy.js',
  },
  expose: {
    ENVIRONMENT: 'local-machine',
  },
  retries: {
    /* Sometimes a flaky test will fail in `cypress run`, which will cause
       all subsequent tests to be pending. Retry a failing test twice to
       make sure it's not just flaky. */
    runMode: 2,
    openMode: 0,
  }
});
