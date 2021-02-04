export class Pagination {

  paginationContent() {
    return cy.get( '.m-pagination' );
  }

  enter( name ) {
    cy.get( '.m-pagination_current-page' ).type( name );
  }

  form() {
    cy.get( '.m-pagination_form' );
  }

  clickNextButton() {
    cy.get( '.m-pagination_btn-next' ).click( { force: true } );
  }

  clickPreviousButton() {
    cy.get( '.m-pagination_btn-prev' ).click( { force: true } );
  }

  clickSubmitButton() {
    cy.get( '.m-pagination_btn-submit' ).click( { force: true } );
  }
}
