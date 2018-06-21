const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/regulations3k';

const app = require( `${ BASE_JS_PATH }/js/search.js` );

describe( 'The Regs3K search page', () => {

  it( 'should not throw any errors on init', () => {
    expect( () => app ).not.toThrow();
  } );

} );
