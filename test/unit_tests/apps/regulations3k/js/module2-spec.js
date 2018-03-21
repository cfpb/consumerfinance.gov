const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/regulations3k';

const module = require( `${ BASE_JS_PATH }/js/module2.js` );

describe( 'Some other module that does something', () => {

  it( 'should not throw any errors on init', () => {
    expect( () => module.init() ).not.toThrow();
  } );

} );
