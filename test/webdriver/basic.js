const assert = require( 'assert' );

describe( 'the cf.gov homepage', () => {
//   it( 'should not have changed visually for small screens', () => {
//     browser.url( 'http://localhost:8000' );
//     browser.setWindowSize( 410, 730 );
//     browser.saveFullPageScreen( 'homepage' );
//     expect( browser.checkFullPageScreen( 'homepage' ) ).toEqual( 0 );
//   } );
  it( 'should not have changed visually for medium screens', () => {
    browser.url( 'http://localhost:8000' );
    browser.setWindowSize( 768, 1024 );
    browser.saveFullPageScreen( 'homepage' );
    expect( browser.checkFullPageScreen( 'homepage' ) ).toEqual( 0 );
  } );
  it( 'should not have changed visually for large screens', () => {
    browser.url( 'http://localhost:8000' );
    browser.setWindowSize( 1280, 1024 );
    browser.saveFullPageScreen( 'homepage' );
    expect( browser.checkFullPageScreen( 'homepage' ) ).toEqual( 0 );
  } );
} );

// describe( 'Example', () => {
//   beforeEach( () => {
//     browser.url( 'https://webdriver.io' );
//   } );

//   it( 'should save some screenshots', () => {
//     // Save a screen
//     // browser.saveScreen( 'homepage', { /* some options */ } );

//     // // Save an element
//     // browser.saveElement( $( '#element-id' ), 'firstButtonElement', { /* some options */ } );

//     // Save a full page screens
//     browser.saveFullPageScreen( 'homepage', { /* some options */ } );
//   } );

//   it( 'should compare successful with a baseline', () => {
//     // Check a screen
//     // expect( browser.checkScreen( 'examplePaged', { /* some options */ } ) ).toEqual( 0 );

//     // // Check an element
//     // expect( browser.checkElement( $( '#element-id' ), 'firstButtonElement', { /* some options */ } ) ).toEqual( 0 );

//     // Check a full page screens
//     expect( browser.checkFullPageScreen( 'homepage', { /* some options */ } ) ).toEqual( 0 );
//   } );
// } );
