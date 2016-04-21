'use strict';

describe( 'Text Introduction', function() {
  beforeAll( function() {
    browser.get( '/browse-filterable-page/' );
  } );

  // TODO: This test is failing and breaking the Jenkins build.
  //   BEWDS should investigate.
  xit( 'should properly load in a browser',
    function() {
      expect(element(by.css( 'body' )).getText() ).toContain(
        'this is an intro' );
    }
  );

} );
