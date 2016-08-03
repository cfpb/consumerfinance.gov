'use strict';

var _getQAElement = require( '../../util/qa-element' ).get;

/* TODO: Create tests for the following organisms:
          - FilterableListControls
          - Sidebar Breakout
          - PostPreviewSnapshot
          - RelatedPosts
*/


/* TODO: More comprehensive test for this organism. */
describe( 'Email Signup', function() {
  beforeAll( function() {
    browser.get( '/sublanding-page/' );
  } );

  it( 'should properly load in a browser',
    function() {
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'Email Sign up' );
    }
  );
} );

/* TODO: More comprehensive test for this organism. */
describe( 'Regulation Comments', function() {
  beforeAll( function() {
    browser.get( '/sublanding-page/' );
  } );

  it( 'should properly load in a browser',
    function() {
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'Enter your comments' );
    }
  );
} );

describe( 'Table', function() {
  beforeAll( function() {
    browser.get( '/browse-filterable-page/learn-page/' );
  } );

  it( 'should properly load in a browser',
    function() {
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'table hyperlink' );
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'table text' );
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'table text blob' );
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'table rich text blob' );
    }
  );
} );

describe( 'Expandable Group', function() {
  beforeAll( function() {
    browser.get( '/browse-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'Expandable Group' );
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'Expandable group body' );
      expect( _getQAElement( 'expandable' ).isPresent() ).toBe( true );
    }
  );
} );

describe( 'Item Introduction', function() {
  beforeAll( function() {
    browser.get( '/browse-filterable-page/learn-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'Item Introduction' );
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'Item introduction body' );
    }
  );
} );
