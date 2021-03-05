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
 * Emulates Tab key navigation
 */
Cypress.Commands.add( 'tab', { prevSubject: 'optional' },
  ( $subject, direction = 'forward', options = {} ) => {
    const thenable = $subject ?
      cy.wrap( $subject, { log: false } ) :
      cy.focused( { log: options.log !== false } );
    thenable
      .then( $el => nextTabbable( $el, direction ) )
      .then( $el => {
        if ( options.log !== false ) {
          Cypress.log( {
            $el,
            name: 'tab',
            message: direction
          } );
        }
      } )
      .focus( { log: false } );
  } );
