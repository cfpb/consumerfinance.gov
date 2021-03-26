export default class EmailSignup {

  open() {
    cy.visit( '/consumer-tools/' );
  }

  signUp( email ) {
    cy.get( '.o-form__email-signup' ).within( () => {
      cy.get( 'input:first' ).type( email );
      cy.get( 'button:first' ).click();
    } );
  }

  successNotification() {
    return cy.get( '.m-notification_message' );
  }
}
