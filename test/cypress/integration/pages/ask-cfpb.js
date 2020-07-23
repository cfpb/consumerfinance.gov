import { AskCfpbSearch } from '../../pages/ask-cfpb/search';

const search = new AskCfpbSearch();

describe( 'Ask CFPB', () => {
  describe( 'Search', () => {
    it( 'should return results', () => {
      search.open();
      search.search( 'security' );
      search.resultsSection().should( 'be.visible' );
    } );
  } );
} );
