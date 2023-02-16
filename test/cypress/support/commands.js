/* ***********************************************
   This example commands.js shows you how to
   create various custom commands and overwrite
   existing commands.

   For more comprehensive examples of custom
   commands please read more here:
   https://on.cypress.io/custom-commands
   ***********************************************


   -- This is a parent command --
   Cypress.Commands.add("login", (email, password) => { ... })


   -- This is a child command --
   Cypress.Commands.add("drag", { prevSubject: 'element'}, (subject, options) => { ... })


   -- This is a dual command --
   Cypress.Commands.add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })


   -- This will overwrite an existing command --
   Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... }) */

import nextTabbable from './nextTabbable';

/**
 * Emulates Tab key navigation.
 */
Cypress.Commands.add(
  'tab',
  { prevSubject: 'optional' },
  ($subject, direction = 'forward', options = {}) => {
    const thenable = $subject
      ? cy.wrap($subject, { log: false })
      : cy.focused({ log: options.log !== false });
    thenable
      .then(($el) => nextTabbable($el, direction))
      .then(($el) => {
        if (options.log !== false) {
          Cypress.log({
            $el,
            name: 'tab',
            message: direction,
          });
        }
      })
      .focus({ log: false });
  }
);

/**
 * Add a command to test whether an element has been scrolled into view.
 */
Cypress.Commands.add('isScrolledTo', { prevSubject: true }, (element) => {
  cy.get(element).should(($el) => {
    const bottom = Cypress.$(cy.state('window')).height();
    const rect = $el[0].getBoundingClientRect();

    expect(rect.top).not.to.be.greaterThan(
      bottom,
      `Expected element not to be below the visible scrolled area`
    );
    expect(rect.top).to.be.greaterThan(
      0 - rect.height,
      `Expected element not to be above the visible scrolled area`
    );
  });
});
