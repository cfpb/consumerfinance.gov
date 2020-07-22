import { RuralOrUnderserved } from '../../pages/rural-or-underserved/rural-or-underserved';

const page = new RuralOrUnderserved();

describe( 'Rural or Underserved', () => {

  describe( 'Address Search', () => {

    it( 'Should render a table for a series of addresses searched', () => {
      page.open();
      page.searchAddress( '1600 Pennsylvania Avenue Washington DC' );
      page.resultsTable().should( 'be.visible' );
    } );

  } );

} );
