const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/regulations3k';

const expect = require( 'chai' ).expect;

const app = require( `${ BASE_JS_PATH }/js/index.js` );

describe( 'The app', function() {

  it( 'should not throw any errors on init', function() {
    expect( () => app ).to.not.throw();
  } );

} );
