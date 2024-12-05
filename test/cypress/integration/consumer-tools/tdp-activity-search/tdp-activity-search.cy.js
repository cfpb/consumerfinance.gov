import { ActivitySearch } from './tdp-activity-search-helpers.cy.js';

const search = new ActivitySearch();

describe('Activity Search', () => {
  it('should filter results', () => {
    search.open();
    search.selectFilter('activity_duration', '1');
    cy.url().should('include', 'activity_duration=1');
    search.clearFilters().should('be.visible');
    search.resultsFilterTag().should('be.visible');
  });

  it('should clear results filters', () => {
    search.open();
    search.selectFilter('activity_duration', '1');
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

  it('should remember filters when a new search query is performed', () => {
    search.open();
    search.search('money');
    search.selectFilter('activity_duration', '1');
    search.resultsFilterTag().should('be.visible');
    search.search('loan');
    cy.url().should('include', 'loan');
    cy.url().should('include', 'activity_duration');
    search.resultsFilterTag().should('be.visible');
  });
});
