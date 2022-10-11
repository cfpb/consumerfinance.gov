import { FindAHousingCounselor } from './find-a-housing-counselor-helpers.cy.js';

const page = new FindAHousingCounselor();

describe( 'Find a housing counselor', () => {
  describe( 'Search by ZIP code', () => {
    beforeEach( () => {
      page.interceptMapboxAPIRequests();
    } );

    it( 'should return nearby counselors', () => {
      page.open();
      page.searchZipCode( '22204' );
      cy.wait( [ '@mapboxStreets', '@mapboxText' ] );
      page.resultsSection().should( 'be.visible' );
    } );
  } );
} );
