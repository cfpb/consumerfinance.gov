const app = require( '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/index.js' );

describe( 'The app', () => {

  it( 'should not throw any errors on init', () => {
    expect( () => app ).not.toThrow();
  } );

} );
