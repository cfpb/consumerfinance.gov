/* eslint-disable no-undef */

describe( 'the cf.gov carousel', () => {
  it( 'should not have changed visually for medium-ish screens', () => {
    browser.url( 'http://localhost:8000' );
    browser.setWindowSize( 800, 600 );
    browser.saveElement( $( '.o-carousel' ), 'carousel' );
    expect( browser.checkScreen( 'carousel' ) ).toEqual( 0 );
  } );
  it( 'should not have changed visually for large-ish screens', () => {
    browser.url( 'http://localhost:8000' );
    browser.setWindowSize( 1024, 768 );
    browser.saveElement( $( '.o-carousel' ), 'carousel' );
    expect( browser.checkScreen( 'carousel' ) ).toEqual( 0 );
  } );
} );
