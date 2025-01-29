export class FilingInstructionGuide {
  url() {
    return '/data-research/small-business-lending/filing-instructions-guide/2024-guide/';
  }

  open() {
    cy.visit(this.url());
  }

  toc() {
    return cy.get('.o-fig .o-fig__sidebar');
  }

  getSection(section) {
    return cy.get(`a[id="${section}"]`);
  }

  getSearchModal() {
    return cy.get('#ctrl-f-modal');
  }

  getSearchButton() {
    return cy.get('#ctrl-f button');
  }

  getSearchInput() {
    return cy.get('#ctrl-f-search-input');
  }

  getSearchInputClearButton() {
    return cy.get('#ctrl-f-clear-button');
  }

  getSearchModalCloseButton() {
    return cy.get('#ctrl-f-close-button');
  }

  getSearchResults() {
    return cy.get('#ctrl-f-search-results');
  }

  getFirstSearchResult() {
    return cy.get('.ctrl-f-search-result a').first();
  }

  getMobileTOCHeader() {
    return cy.get('.o-fig__sidebar .o-secondary-nav__header');
  }

  getMobileTOCBody() {
    return cy.get('.o-secondary-nav__content');
  }

  goToSection(section) {
    return this.getSection(section).scrollIntoView({ duration: 1000 });
  }

  getNavItem(section) {
    return cy.get(`a.o-secondary-nav__link[href="#${section}"]`);
  }

  clickNavItem(section) {
    return this.getNavItem(section).click();
  }

  clickSectionHeading(section) {
    return this.getSection(section).click();
  }

  expectSectionInViewport(section) {
    return this.getSection(section).isWithinViewport();
  }

  expectSectionNotInViewport(section) {
    return this.getSection(section).isNotWithinViewport();
  }

  toggleToc() {
    return cy.get('.o-secondary-nav__header').click();
  }

  scrollToBottom() {
    return cy.get('.o-fig__heading').last().scrollIntoView();
  }

  getUnrenderedListTags() {
    return cy.get('.o-fig').contains('<li>');
  }

  getUnrenderedBrTags() {
    return cy.get('.o-fig').contains('<br>');
  }

  getUnrenderedPTags() {
    return cy.get('.o-fig').contains('<p>');
  }
}
