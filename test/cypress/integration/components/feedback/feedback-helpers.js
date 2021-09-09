export class Feedback {

  open() {
    cy.visit( '/owning-a-home/feedback' );
  }

  submitComment( comment ) {
    cy.get( '#comment' ).type( comment );
    cy.get( '.content_main' )
      .within( () => {
        cy.get( 'form' ).submit();
      } );
  }

  successNotification() {
    return cy.get( '.content_main' )
      .within( () => cy.get( '.m-notification' ) );
  }

}
