export class RegulationsSearch {

  open() {
    cy.visit( '/rules-policy/regulations/search-regulations/results/' );
  }

  searchForm() {
    return cy.get( 'form[action="."]' );
  }

  searchTerm( term ) {
    this.searchForm().find( '#query' ).type( term );
    this.searchForm().submit();
  }

  searchResults() {
    return cy.get( '#regs3k-results' );
  }

  setPageSize( size ) {
    cy.get( 'span' ).contains( 'Results per page' ).click();
    cy.get( `#results_${ size }` ).check( { force: true } );
  }

  searchResult() {
    return cy.get( '.results_item' );
  }

  selectRegulation( regulationNumber ) {
    cy.get( `#regulation-${ regulationNumber }` ).check( { force: true } );
  }

  filters() {
    return cy.get( '.filters_applied' );
  }

}
