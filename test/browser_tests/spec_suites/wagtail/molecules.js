'use strict';

describe( 'Text Introduction', function() {
  beforeAll( function() {
    browser.get( '/browse-filterable-page/' );
  } );

  it( 'should properly load in a browser',
    function() {
      expect( element(by.css( 'body' ) ).getText() )
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
      expect(element(by.css( 'body' )).getText() ).toContain(
        'this is a featured content body' );
    }
  );

} );

describe( 'Expandable', function() {
  beforeAll( function() {
    browser.get( '/browse-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect(element(by.css( 'body' )).getText() ).toContain(
        'this is an expandable' );
    }
  );

} );


describe( 'Related Links', function() {
  beforeAll( function() {
    browser.get( '/demo-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect(element(by.css( 'body' )).getText() ).toContain(
        'this is a related link' );
    }
  );

} );

describe( 'Related Metadata', function() {
  beforeAll( function() {
    browser.get( '/browse-filterable-page/document-detail-page' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect(element(by.css( 'body' )).getText() ).toContain(
        'this is a related metadata heading' );
    }
  );

} );

describe( 'Quote', function() {
  beforeAll( function() {
    browser.get( '/browse-filterable-page/learn-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect(element(by.css( 'body' )).getText() ).toContain(
        'this is a quote' );
    }
  );

} );

describe( 'Call to Action', function() {
  beforeAll( function() {
    browser.get( '/browse-filterable-page/learn-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect(element(by.css( 'body' )).getText() ).toContain(
        'this is a call to action' );
    }
  );

} );

describe( 'Call to Action', function() {
  beforeAll( function() {
    browser.get( '/sublanding-filterable-page/' );
  } );
  it( 'should properly load in a browser',
    function() {
      expect(element(by.css( 'body' )).getText() ).toContain(
        'this is a hero heading' );
    }
  );

} );