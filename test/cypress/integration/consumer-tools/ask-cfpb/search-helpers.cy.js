export class AskCfpbSearch {
  open(language) {
    const path = language === 'es' ? '/es/obtener-respuestas/' : '/ask-cfpb/';
    cy.visit(path);
  }

  searchInputComponent() {
    return cy.get('[data-cy=ask-search-form] .o-search-input');
  }

  input() {
    return this.searchInputComponent().find('input');
  }

  enter(term) {
    this.input().type(term);
  }

  autocomplete() {
    return cy.get('.m-autocomplete__results');
  }

  submitButton() {
    return this.searchInputComponent().find('button[type="submit"]');
  }

  resetButton() {
    return this.searchInputComponent().find('button[type="reset"]');
  }

  search() {
    this.submitButton().click();
  }

  clearSearch() {
    this.resetButton().click();
  }

  resultsSection() {
    return cy.get('.search-results');
  }

  resultsHeader() {
    return cy.get('.results-header');
  }

  maxLengthErrorMessage() {
    return cy.get('#o-search-bar_error-message');
  }

  longTerm() {
    const maxLength = Cypress.$('#o-search-bar_query').attr('maxlength');
    const longTerm = new Array(parseInt(maxLength, 10) + 1).join('c');
    return longTerm;
  }
}
