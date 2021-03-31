import { FindAHousingCounselor } from '../../../pages/consumer-tools/find-a-housing-counselor';

const page = new FindAHousingCounselor();

describe( 'Find a housing counselor', () => {
  describe( 'Search by ZIP code', () => {
    it( 'should return nearby counselors', () => {
      page.open();
      page.searchZipCode( '22204' );
      page.resultsSection().should( 'be.visible' );
    } );
  } );
} );
