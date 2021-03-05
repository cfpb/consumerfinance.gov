import { ActivitySearch } from '../../../pages/consumer-tools/activity-search';

const search = new ActivitySearch();

describe( 'Activity Search', () => {
  it( 'should filter results', () => {
    const resultsFilterText = 'financial-habits-and-norms';
    search.open();
    search.selectFilter( 'Financial habits and norms' );
    search.clearFilters().should( 'be.visible' );
    search.resultsFilterTag( resultsFilterText ).should( 'be.visible' );
  } );
  it( 'should clear results filters', () => {
    const resultsFilterText = 'financial-habits-and-norms';
    search.open();
    search.selectFilter( 'Financial habits and norms' );
    search.resultsFilterTag( resultsFilterText ).should( 'be.visible' );
    search.clearFilters().click();
    search.resultsFilterTag( resultsFilterText ).should( 'not.exist' );
  } );
  it( 'should show no search results when no results', () => {
    search.open();
    search.search( 'notaword' );
    search.resultsCountEmpty().should( 'be.visible' );
  } );
  it( 'should limit results by search query', () => {
    search.open();
    search.search( 'money' );
    cy.url().should( 'include', 'money' );
  } );
} );

