export class FilingInstructionGuide {
  url() {
    return Cypress.env('FIG_URL');
  }

  open() {
    cy.visit(this.url());
  }

  toc() {
    return cy.get('.o-fig .content_sidebar');
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
    return cy.get('.o-fig_sidebar .o-expandable_header');
  }

  getMobileTOCBody() {
    return cy.get('.o-fig_sidebar .o-expandable_content');
  }

  goToSection(section) {
    return this.getSection(section).scrollIntoView({ duration: 1000 });
  }

  getNavItem(section) {
    return cy.get(`a.m-nav-link[href="#${section}"]`);
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
    return cy.get('.o-expandable_header').click();
  }

  scrollToBottom() {
    return cy.get('footer').scrollIntoView();
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
