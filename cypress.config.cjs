const { defineConfig } = require('cypress');

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
      on('before:browser:launch', (browser = {}, launchOptions = {}) => {
        // Log browser info. This could be useful when comparing local to CI.
        console.log('Launching browser', browser);

        if (browser.family === 'chromium' && browser.name !== 'electron') {
          // Auto open devtools.
          launchOptions.args.push('--auto-open-devtools-for-tabs');
        }

        if (browser.family === 'firefox') {
          // Auto open devtools.
          launchOptions.args.push('-devtools');
        }

        if (browser.name === 'electron') {
          // Auto open devtools.
          launchOptions.preferences.devTools = true;
        }

        // Whatever you return here becomes the launchOptions.
        return launchOptions;
      });
    },
  },
  component: {
    specPattern: 'test/cypress/component/**/*.cy.{js,jsx,ts,tsx}',
    excludeSpecPattern: 'test/cypress/component/**/*-helpers.cy.js',
  },
  env: {
    ENVIRONMENT: 'local-machine',
  },
});
