import { ActivitySearch } from '../../pages/practitioner-resources/activity-search';

const search = new ActivitySearch();

describe( 'Practitioner Resources', () => {

  describe( 'Activity Search', () => {
    it( 'should filter results', () => {
      search.open();
      search.selectFilter( 'Financial habits and norms' );
      search.clearFilters().should( 'be.visible' );
      search.clearFilters().click();
    } );
    it( 'should limit results by search query', () => {
      search.open();
      search.search( 'money' );
      cy.url().should( 'include', 'money' );
    } );
  } );

} );
