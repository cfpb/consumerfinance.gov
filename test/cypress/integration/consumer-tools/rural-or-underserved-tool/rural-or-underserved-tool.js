import { RuralOrUnderservedTool } from './rural-or-underserved-tool-helpers';

const page = new RuralOrUnderservedTool();

describe( 'Rural or Underserved Tool', () => {

  describe( 'Address Search', () => {

    it( 'Should render a table for a single address', () => {
      page.open();
      page.searchAddress( '1600 Pennsylvania Avenue Washington DC' );
      page.interceptCensusAPIRequests();
      page.resultsTable().should( 'be.visible' );
    } );

  } );

} );
