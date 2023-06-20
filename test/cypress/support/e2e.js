/* ***********************************************************
   This example support/index.js is processed and
   loaded automatically before your test files.

   This is a great place to put global configuration and
   behavior that modifies Cypress.

   You can change the location of this file or turn off
   automatically serving support files with the
   'supportFile' configuration option.

   You can read more here:
   https://on.cypress.io/configuration
   *********************************************************** */

// Import commands.js using ES2015 syntax:
import './commands';

/* Alternatively you can use CommonJS syntax:
   require('./commands') */

// Import assertions
import './assertions';

// Require skip-test
require('@cypress/skip-test/support');

// Fail Cypress tests fast on the first failure.
import 'cypress-fail-fast';

// Store logs.
let logs = '';

Cypress.on('window:before:load', (window) => {
  // Get your app's iframe by id.
  // This is the frame ID as the page appears in the Cypress app.
  const docIframe = window.parent.document.getElementById(
    "Your project: 'Test Project'"
  );

  // Get the window object inside of the iframe.
  const appWindow = docIframe.contentWindow;

  // This is where I overwrite all of the console methods.
  ['log', 'info', 'error', 'warn', 'debug'].forEach((consoleProperty) => {
    appWindow.console[consoleProperty] = function (...args) {
      /*
       * The args parameter will be all of the values passed as arguments to
       * the console method.
       */
      logs += args.join(' ') + '\n';
    };
  });
});

// Cypress doesn't have a each test event
// so we're using mochas events to clear log state after every test.
Cypress.mocha.getRunner().on('test', () => {
  // Every test reset your logs to be empty.
  // This will make sure only logs from that test suite will be logged if an
  // error happens.
  logs = '';
});

// On a cypress fail. I add the console logs, from the start of test or after
// the last test fail to the current fail,
// to the end of the error.stack property.
Cypress.on('fail', (error) => {
  error.stack += '\nConsole Logs:\n========================';
  error.stack += logs;
  // Clear logs after fail so we dont see duplicate logs.
  logs = '';
  // Still need to throw the error so tests wont be marked as a pass.
  throw error;
});
