const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/regulations3k';

const expect = require( 'chai' ).expect;

const module = require( `${ BASE_JS_PATH }/js/module2.js` );

describe( 'Some other module that does somthing', function() {

  it( 'should not throw any errors on init', function() {
    expect( () => module.init() ).to.not.throw();
  } );

} );
