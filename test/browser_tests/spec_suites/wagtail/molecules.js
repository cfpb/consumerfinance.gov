'use strict';

var _getQAElement = require( '../../util/qa-element' ).get;

describe( 'Text Introduction', function() {
  beforeAll( function() {
    browser.get( '/browse-filterable-page/' );
  } );

  it( 'should properly load in a browser',
    function() {
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'this is an intro' );
    }
  );

} );

describe( 'Featured Content', function() {
  beforeAll( function() {
    browser.get( '/browse-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'this is a featured content body' );
    }
  );

} );

describe( 'Expandable', function() {
  beforeAll( function() {
    browser.get( '/browse-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( _getQAElement( 'expandable' ).isPresent() ).toBe( true );
    }
  );

} );


describe( 'Related Links', function() {
  beforeAll( function() {
    browser.get( '/landing-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'this is a related link' );
    }
  );

} );

describe( 'Related Metadata', function() {
  beforeAll( function() {
    browser.get( '/browse-filterable-page/document-detail-page' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'this is a related metadata heading' );
    }
  );

} );

describe( 'Quote', function() {
  beforeAll( function() {
    browser.get( '/browse-filterable-page/learn-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'this is a quote' );
    }
  );

} );

describe( 'Call to Action', function() {
  beforeAll( function() {
    browser.get( '/browse-filterable-page/learn-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'this is a call to action' );
    }
  );

} );

describe( 'Hero', function() {
  beforeAll( function() {
    browser.get( '/sublanding-filterable-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( element( by.css( 'body' ) ).getText() )
        .toContain( 'this is a hero heading' );
    }
  );

} );

describe( 'Half Width Link Blob', function() {
  beforeAll( function() {
    browser.get( '/landing-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( _getQAElement( 'half-width-link-blob' )
        .isPresent() ).toBe( true );
    }
  );
} );

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

describe( 'Contact', function() {
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

describe( 'RSS Feed', function() {
  beforeAll( function() {
    browser.get( '/sublanding-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect( _getQAElement( 'rss-subscribe-section' )
        .isPresent() ).toBe( true );
    }
  );

} );
