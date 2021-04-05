export class AskCfpbSearch {

  open() {
    cy.visit( '/ask-cfpb/' );
  }

  enter( term ) {
    cy.get( '#o-search-bar_query' ).type( term );
  }

  autocomplete() {
    return cy.get( '.m-autocomplete_results' );
  }

  search() {
    cy.get( '.o-search-bar .a-btn' ).click();
  }

  resultsSection() {
    return cy.get( '.search-results' );
  }

  resultsHeader() {
    return cy.get( '.results-header' );
  }
}
