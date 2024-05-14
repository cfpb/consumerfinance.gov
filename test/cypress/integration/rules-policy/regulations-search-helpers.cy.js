export class RegulationsSearch {
  open() {
    cy.visit('/rules-policy/regulations/search-regulations/results/');
  }

  searchInputComponent() {
    return cy.get('[data-cy=regs-search-form] .o-search-input');
  }

  input() {
    return this.searchInputComponent().find('input');
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

  searchTerm(term) {
    this.input().type(term);
    this.search();
  }

  searchResults() {
    return cy.get('#regs3k-results');
  }

  setPageSize(size) {
    cy.get('span').contains('Results per page').click();
    cy.get(`#results-${size}`).check({ force: true });
  }

  searchResult() {
    return cy.get('.results__item');
  }

  selectRegulation(regulationNumber) {
    cy.get(`#regulation-${regulationNumber}`).check({ force: true });
  }

  filters() {
    return cy.get('.filters__applied');
  }
}
