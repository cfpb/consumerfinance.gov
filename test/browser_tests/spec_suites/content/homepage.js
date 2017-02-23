'use strict';

function _getStylesheets() {
  var sheets = document.styleSheets;
  var hrefs = [];

  for ( var i = 0; i < sheets.length; i++ ) {
    hrefs.push( sheets[i].href );
  }

  return hrefs;
}

describe( 'The homepage', function() {

  beforeEach( function() {
    browser.get( '/' );
  } );

  it( 'should load the stylesheet', function() {
    browser.executeScript( _getStylesheets ).then(
      function( styleSheets ) {
        browser.styleSheets = styleSheets;

        browser.getCapabilities().then( function( cap ) {
          browser.name = cap.get( 'browserName' );
          browser.version = cap.get( 'version' );

          var stylesheet = browser.baseUrl + '/static/css';

          if ( browser.name === 'internet explorer' &&
               browser.version === '8' ) {
            stylesheet += '/main.ie.css';
          } else {
            stylesheet += '/main.css';
          }

          expect( browser.styleSheets ).toContain( stylesheet );
        } );
      } );
  } );
} );
