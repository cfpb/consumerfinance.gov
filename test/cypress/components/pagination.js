export class Pagination {

  clickButton( name ) {
    return cy.get( `.m-pagination_btn-${ name }` )
      .click( { force: true } );
  }

  enter( name ) {
    cy.get( '#m-pagination_current-page-0' )
      .clear( { force: true } ).type( name );
    cy.get( '.m-pagination' )
      .within( () => {
        cy.get( '.m-pagination_form' ).submit();
      } );
  }

  firstPagination() {
    cy.get( '[aria-label="Pagination"]' ).first();
  }

  paginationLabel() {
    cy.get( 'label[for="m-pagination_current-page-0"]' );
  }
}
