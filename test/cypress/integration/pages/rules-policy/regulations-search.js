import { RegulationsSearch } from '../../../pages/rules-policy/regulations-search';

const regulationsSearch = new RegulationsSearch();

describe( 'Policy Compliance', () => {

  describe( 'Regulations Search', () => {

    it( 'should return results based on search term', () => {
      regulationsSearch.open();
      regulationsSearch.searchTerm( 'mortgage' );
      regulationsSearch.searchResults().should( 'be.visible' );
    } );

    it( 'should adjust results based on the page size', () => {
      regulationsSearch.setPageSize( 50 );
      regulationsSearch.searchResult().should( 'have.length', '50' );
    } );

    it( 'should limit results based on regulation', () => {
      regulationsSearch.selectRegulation( 1008 );
      regulationsSearch.filters().should( 'be.visible' );
      regulationsSearch.filters().should( 'contain', 1008 );
    } );

  } );

} );
