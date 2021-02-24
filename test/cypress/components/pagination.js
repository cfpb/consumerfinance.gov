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

  lastResults() {
    cy.get( '.m-pagination_form .u-visually-hidden' )
      .invoke( 'text' ).then( $el => {
        const lastPage = $el.toString().trim().split( ' ' )[3];
        this.enter( lastPage );
      } );
  }

  currentPageLabel() {
    cy.get( 'label[for="m-pagination_current-page-0"]' );
  }

  paginationLabel() {
    cy.get( '[aria-label="Pagination"]' );
  }

}
