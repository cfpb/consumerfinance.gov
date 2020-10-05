import { AskCfpbSearch } from '../../pages/ask-cfpb/search';

const search = new AskCfpbSearch();

describe( 'Ask CFPB', () => {
  describe( 'Search', () => {
    it( 'should autocomplete results', () => {
      search.open();
      search.enter( 'security' );
      search.autocomplete().should( 'be.visible' );
    } );

    it( 'should return results', () => {
      search.open();
      search.enter( 'security' );
      search.search();
      search.resultsSection().should( 'be.visible' );
    } );

    it( 'should correct spelling', () => {
      search.open();
      search.enter( 'vehile' );
      search.search();
      search.resultsHeader().contains( 'results for “vehicle”' );
      search.resultsHeader().siblings('p').first().contains( 'Search instead for' );
    } );
  } );
} );
