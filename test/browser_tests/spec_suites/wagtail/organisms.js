'use strict';

var _getQAElement = require( '../../util/qa-element' ).get;

/* TODO: Create tests for the following organisms:
          - FilterableListControls
          - Sidebar Breakout
          - PostPreviewSnapshot
          - RelatedPosts
*/


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
