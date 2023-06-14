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
    // setupNodeEvents can be defined in either
    // the e2e or component configuration.
    setupNodeEvents(on, config) {
      on('before:browser:launch', (browser = {}, launchOptions = {}) => {
        // Log browser info. This could be useful when comparing local to CI.
        // console.log('Launching browser', browser);

        // Auto open devtools.
        if (browser.family === 'chromium') {
          if (browser.name === 'electron')
            launchOptions.preferences.devTools = true;
          else launchOptions.args.push('--auto-open-devtools-for-tabs');
        } else if (browser.family === 'firefox') {
          launchOptions.args.push('-devtools');
        }

        // Whatever you return here becomes the launchOptions.
        return launchOptions;
      });

      // IMPORTANT return the updated config object.
      return config;
    },
    baseUrl: 'http://localhost:8000',
    specPattern: 'test/cypress/integration/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'test/cypress/support/e2e.js',
    excludeSpecPattern: 'test/cypress/integration/**/*-helpers.cy.js',
  },
  component: {
    specPattern: 'test/cypress/component/**/*.cy.{js,jsx,ts,tsx}',
    excludeSpecPattern: 'test/cypress/component/**/*-helpers.cy.js',
  },
  env: {
    ENVIRONMENT: 'local-machine',
  },
});
