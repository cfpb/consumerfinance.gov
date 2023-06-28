import { ActivitySearch } from './tdp-activity-search-helpers.cy.js';

const search = new ActivitySearch();

describe('Activity Search', () => {
  it('should filter results', () => {
    search.open();
    search.selectFilter('grade_level', '4');
    cy.url().should('include', 'grade_level=4');
    search.clearFilters().should('be.visible');
    search.resultsFilterTag().should('be.visible');
  });

  it('should clear results filters', () => {
    search.open();
    search.selectFilter('grade_level', '4');
    search.resultsFilterTag().should('be.visible');
    search.clearFilters().click();
    search.resultsFilterTag().should('not.exist');
  });

  it('should show no search results when no results', () => {
    search.open();
    search.search('notaword');
    search.resultsCountEmpty().should('be.visible');
  });

  it('should limit results by search query', () => {
    search.open();
    search.search('money');
    cy.url().should('include', 'money');
  });
});
