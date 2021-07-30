export class AskCfpbSearch {

  open() {
    cy.visit( '/ask-cfpb/' );
  }

  input() {
    return cy.get( '#o-search-bar_query' );
  }

  enter( term ) {
    this.input().type( term );
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

  maxLengthErrorMessage() {
    return cy.get( '#o-search-bar-error_message' );
  }
}
