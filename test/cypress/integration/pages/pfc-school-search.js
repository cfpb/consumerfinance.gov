import { PfcSchoolSearch } from '../../pages/paying-for-college/school-search';

const page = new PfcSchoolSearch();

describe( 'Paying For College Search', () => {
  it( 'should return results', () => {
    page.open();
    page.click( 'Get started' )
    page.enter( 'American' );
    page.searchResults().should( 'be.visible' );
} );

  // it( 'should contain results', () => {
  //   page.open();
  //   page.click( 'Get started' )
  //   page.select( 'ABC' );
  //   page.searchResults().should( 'be.visible' );
  //   page.searchResults().contains( 'ABCO Technology' );
  // } );
} );
