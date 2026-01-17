export class ExploreRates {
  selectState(state) {
    cy.get('#location').select(state);
  }

  selectRateType(val) {
    this.getRateTypeSelector().select(val);
  }

  selectLoanType(val) {
    this.getLoanTypeSelector().select(val);
  }

  selectCounty(val) {
    this.getCountySelector().select(val);
  }

  getHousePriceInput() {
    return cy.get('#house-price');
  }

  getCountySelector() {
    return cy.get('#county');
  }

  getCountyAlert() {
    return cy.get('#county-warning');
  }

  getHighBalanceAlert() {
    return cy.get('#hb-warning');
  }

  // Loan type and term drop-down menus.
  getRateTypeSelector() {
    return cy.get('#rate-structure');
  }

  getLoanTermSelector() {
    return cy.get('#loan-term');
  }

  getLoanTypeSelector() {
    return cy.get('#loan-type');
  }

  getArmTypeSelector() {
    return cy.get('#arm-type');
  }

  // Main graph area.
  getGraph() {
    return cy.get('#chart-section').within(() => cy.get('figure:first'));
  }

  getChartResultAlert() {
    return cy.get('#chart-result-alert');
  }
}
