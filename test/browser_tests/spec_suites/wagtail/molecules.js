'use strict';

var _getQAElement = require( '../../util/qa-element' ).get;




describe( 'Image Text 50 50', function() {
  beforeAll( function() {
    browser.get( '/landing-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( _getQAElement( 'image-text-50-50' ).isPresent() ).toBe( true );
    }
  );
} );

describe( 'Image Text 25 75', function() {
  beforeAll( function() {
    browser.get( '/landing-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( _getQAElement( 'image-text-25-75' ).isPresent() ).toBe( true );
    }
  );
} );

describe( 'FormField With Button', function() {
  beforeAll( function() {
    browser.get( '/sublanding-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( _getQAElement( 'formfield-with-button' )
        .isPresent() ).toBe( true );
    }
  );
} );

