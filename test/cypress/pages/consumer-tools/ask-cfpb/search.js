export class AskCfpbSearch {

  open( language ) {
    const path = language === 'es' ? '/es/obtener-respuestas/' : '/ask-cfpb/';
    cy.visit( path );
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

  submitButton() {
    return cy.get( '.o-search-bar .a-btn' );
  }

  search() {
    this.submitButton().click();
  }

  resultsSection() {
    return cy.get( '.search-results' );
  }

  resultsHeader() {
    return cy.get( '.results-header' );
  }

  maxLengthErrorMessage() {
    return cy.get( '#o-search-bar_error-message' );
  }

  longTerm() {
    const maxLength = Cypress.$( '#o-search-bar_query' ).attr( 'maxlength' );
    const longTerm = new Array( parseInt( maxLength, 10 ) + 1 ).join( 'c' );
    return longTerm;
  }
}
