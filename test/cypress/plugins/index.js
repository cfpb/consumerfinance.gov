/* / <reference types="cypress" />
    ***********************************************************
    This example plugins/index.js can be used to load plugins

    You can change the location of this file or turn off loading
    the plugins file with the 'pluginsFile' configuration option.

    You can read more here:
    https://on.cypress.io/plugins-guide
    *********************************************************** */

/* This function is called when a project is opened or re-opened (e.g. due to
   the project's config changing) */

/**
 * @type {Cypress.PluginConfig}
 * @param {object} on - hook into various events Cypress emits.
 * @param {object} config - the resolved Cypress config.
 */
// eslint-disable-next-line no-unused-vars
module.exports = (on, config) => {
  // Workaround to show devtools in failure screenshots.
  // See https://github.com/cypress-io/cypress/issues/2024#issuecomment-754571301
  on('before:browser:launch', (browser = {}, launchOptions) => {
    if (browser.family === 'chromium' && browser.name !== 'electron') {
      // auto open devtools
      launchOptions.args.push('--auto-open-devtools-for-tabs');
    }

    if (browser.family === 'firefox') {
      // auto open devtools
      launchOptions.args.push('-devtools');
    }

    if (browser.name === 'electron') {
      // auto open devtools
      launchOptions.preferences.devTools = true;
    }

    // whatever you return here becomes the launchOptions
    return launchOptions;
  });
};
