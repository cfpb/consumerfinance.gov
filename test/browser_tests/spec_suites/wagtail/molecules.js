'use strict';

describe( 'Text Introduction', function() {
  beforeAll( function() {
    browser.get('/browse-filterable-page/');
  } );
  it( 'should properly load in a browser',
    function() {
      expect(element(by.css('body')).getText()).toContain(
        'this is an intro' );
    }
  );

} );



