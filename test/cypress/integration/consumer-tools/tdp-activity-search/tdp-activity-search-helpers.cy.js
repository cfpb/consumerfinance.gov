export class ActivitySearch {
  open() {
    cy.visit(
      '/consumer-tools/educator-tools/youth-financial-education/teach/activities/',
    );
  }

  selectFilter(name, value) {
    cy.get(`input[name="${name}"][value="${value}"]`).check({ force: true });
  }

  clearFilters() {
    return cy.get('.results_filters-clear');
  }

  resultsFilterTag() {
    return cy.get('[data-value="#activity_duration--15-20-minutes"]');
  }

  resultsCountEmpty() {
    return cy.get('.results_count__empty');
  }

  search(term) {
    cy.get('#search-text').type(term);
    cy.get('form[action="."]')
      .first()
      .within(() => {
        cy.get('button').first().click();
      });
  }
}
