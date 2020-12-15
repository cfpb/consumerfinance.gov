import { AskCfpbSearch } from '../../pages/ask-cfpb/search';

const search = new AskCfpbSearch();

describe( 'Ask CFPB', () => {
  beforeEach( () => {
    search.open();
  } );
  describe( 'Search', () => {
    it( 'should autocomplete results', () => {
      search.enter( 'security' );
      search.autocomplete().should( 'be.visible' );
    } );

    it( 'should return results', () => {
      search.enter( 'security' );
      search.search();
      search.resultsSection().should( 'be.visible' );
    } );

    it( 'should correct spelling', () => {
      search.enter( 'vehile' );
      search.search();
      search.resultsHeader().should( 'contain', 'results for “vehicle”' );
      search.resultsHeader().siblings( 'p' ).first().should( 'contain', 'Search instead for' );
    } );
  } );
} );
