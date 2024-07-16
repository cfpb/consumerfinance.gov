export class ExploreCreditCards {
  openLandingPage() {
    cy.visit('/consumer-tools/credit-cards/explore-cards/');
  }

  openResultsPage(filterParams) {
    const url =
      '/consumer-tools/credit-cards/explore-cards/cards/?' +
      new URLSearchParams(filterParams).toString();
    cy.visit(url);
  }

  selectCreditTier(tier) {
    cy.get('select[name=credit_tier]').select(tier);
  }

  selectLocation(location) {
    cy.get('select[name=location]').select(location);
  }

  selectSituation(situation) {
    cy.get('input[name=situations]').check(situation, { force: true });
  }

  selectOrdering(ordering) {
    cy.get('#tccp-ordering select').select(ordering);
  }

  clickSubmitButton() {
    cy.get('button').contains('See cards for your situation').click();
  }

  openFilterExpandable() {
    cy.get('.o-filterable-list-controls button.o-expandable__header').click();
  }

  clickShowMoreButton() {
    cy.get('button')
      .contains('Show more results with higher interest rates')
      .click();
  }

  getOrderingDropdownValue() {
    return cy.get('#tccp-ordering select').find('option:selected');
  }

  getNumberResults() {
    return new Promise((resolve) => {
      return cy
        .get('.htmx-container')
        .not('.htmx-request')
        .get('.o-filterable-list-results .m-notification')
        .then((el) => resolve(Number(el.text().replace(/[^0-9]/g, ''))));
    });
  }

  getNumberVisibleSpeedBumps() {
    return new Promise((resolve) => {
      return cy
        .get('.htmx-container')
        .not('.htmx-request')
        .get('.o-well--speed-bump')
        .filter(':visible')
        .then((el) => resolve(el.length));
    });
  }

  getNumberVisibleResults() {
    return new Promise((resolve) => {
      return cy
        .get('.htmx-container')
        .not('.htmx-request')
        .get('.m-card--tabular')
        .filter(':visible')
        .then((el) => resolve(el.length));
    });
  }

  selectCheckboxFilter(name, value) {
    cy.get(`input[name=${name}]`).check(value, { force: true });
  }

  checkA11y() {
    cy.injectAxe();
    cy.checkA11y();
  }
}
