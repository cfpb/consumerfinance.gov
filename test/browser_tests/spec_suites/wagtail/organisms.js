'use strict';

var _getQAElement = require( '../../util/qa-element' ).get;

/* TODO: Create tests for the following organisms:
          - FilterableListControls
          - Sidebar Breakout
          - PostPreviewSnapshot
          - RelatedPosts
*/



describe( 'Main Contact Info', function() {
  beforeAll( function() {
    browser.get( '/sublanding-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( _getQAElement( 'contact-address' ).isPresent() ).toBe( true );
      expect( _getQAElement( 'contact-email' ).isPresent() ).toBe( true );
      expect( _getQAElement( 'contact-phone' ).isPresent() ).toBe( true );
    }
  );
} );

describe( 'Sidebar Contact Info', function() {
  beforeAll( function() {
    browser.get( '/landing-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( _getQAElement( 'contact-address' ).isPresent() ).toBe( true );
      expect( _getQAElement( 'contact-email' ).isPresent() ).toBe( true );
      expect( _getQAElement( 'contact-phone' ).isPresent() ).toBe( true );
    }
  );
} );

describe( 'Full Width Text', function() {
  beforeAll( function() {
    browser.get( '/browse-filterable-page/learn-page/' );
  } );

  it( 'should properly load in a browser',
    function() {
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'Full width text content' );
      expect( element( by.css( '.o-full-width-text-group' ) ).getText() )
        .toContain( 'this is a quote' );
      expect( element( by.css( '.o-full-width-text-group' ) ).getText() )
        .toContain( 'A CITATION' );
    }
  );
} );

describe( 'Image Text 25 75 Group', function() {
  beforeAll( function() {
    browser.get( '/landing-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'Image 25 75 Group' );
      expect( _getQAElement( 'image-text-25-75' ).isPresent() ).toBe( true );
    }
  );
} );

describe( 'Image Text 50 50 Group', function() {
  beforeAll( function() {
    browser.get( '/landing-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'Image 50 50 Group' );
      expect( _getQAElement( 'image-text-50-50' ).isPresent() ).toBe( true );
    }
  );
} );

describe( 'Half Width Link Blob Group', function() {
  beforeAll( function() {
    browser.get( '/landing-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'Half Width Link Blob Group' );
      expect( _getQAElement( 'half-width-link-blob' )
        .isPresent() ).toBe( true );
    }
  );
} );

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
