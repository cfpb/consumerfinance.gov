export class PfcFinancialPathToGraduation {
  clickGetStarted() {
    cy.get('.btn__get-started').click();
  }

  nextToSchoolCosts() {
    cy.get('.a-btn--next[data-destination="school-costs"]').click();
  }

  nextToSeeCustomized() {
    cy.get('.a-btn--next[data-destination="debt-guideline"]').click();
  }

  skipToCustomized() {
    cy.get(
      '.college-costs__buttons--next[data-destination="customize-estimate"]',
    ).click();
  }

  chooseAndSet() {
    this.enter('Harvard University');
    this.clickSearchResult('Harvard University');
    this.setIncome('48k-75k');
  }

  enter(name) {
    /* The following pastes the `name` value into the input and manually fires
       the keyup event. This is used so that the search-schools API is only
       called once, instead of each time a key is typed in. This prevents
       several API calls from occurring in the tests, which made them flaky.
    */
    cy.get('#search__school-input').invoke('val', name).trigger('keyup');
  }

  searchResults() {
    return cy.get('#search-results');
  }

  clickSearchResult(name) {
    cy.contains('#search-results button', name).click();
    cy.get('#search-results').should('not.be.visible');
  }

  typeText(name, value) {
    cy.get(`#${name}`).type(value);
  }

  clickLeftNav(name) {
    cy.get(`[data-nav_section="${name}"]`).click();
  }

  setText(name, value) {
    cy.get(`#${name}`).clear();
    cy.get(`#${name}`).type(value);
  }

  setIncome(val) {
    cy.get('#program-income').select(val);
  }

  selectProgram(program, name) {
    cy.get(`#program-${program}-radio_${name} + label`).click();
  }

  affordLoanChoice(name) {
    cy.get(`#affording-loans-choices_${name}`).check({ force: true });
  }

  actionPlan(name) {
    cy.get(`#action-plan_${name}`).check({ force: true });
  }

  enterProgramDetails() {
    this.enter('Harvard University');
    this.searchResults().should('be.visible');
    this.clickSearchResult('Harvard University');
    this.selectProgram('type', 'certificate');
    this.selectProgram('years-spent', 'n');
    this.selectProgram('length', '1');
    this.selectProgram('housing', 'on-campus');
    this.selectProgram('dependency', 'dependent');
  }
}
