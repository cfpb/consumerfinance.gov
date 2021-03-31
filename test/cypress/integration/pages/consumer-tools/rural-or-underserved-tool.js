import { RuralOrUnderservedTool } from '../../../pages/consumer-tools/rural-or-underserved-tool';

const page = new RuralOrUnderservedTool();

describe( 'Rural or Underserved Tool', () => {

  describe( 'Address Search', () => {

    it( 'Should render a table for a series of addresses searched', () => {
      page.open();
      page.searchAddress( '1600 Pennsylvania Avenue Washington DC' );
      page.resultsTable().should( 'be.visible' );
    } );

  } );

} );
