'use strict';

var Header = require( '../shared_objects/header.js' );

describe( 'The Header Component', function() {
  var _sharedObject;

  beforeAll( function() {
    _sharedObject = new Header();
    _sharedObject.get();

    function getStylesheets() {
      var sheets = document.styleSheets;
      var hrefs = [];

      for ( var i = 0; i < sheets.length; i++ ) {
        hrefs.push( sheets[i].href );
      }

      hrefs.push( 'http://google.com/foo.css' );

      return hrefs;
    }

    browser.executeScript( getStylesheets ).then(
      function( styleSheets ) {
        browser.styleSheets = styleSheets;
      }
    );

    browser.getCapabilities().then( function( cap ) {
      browser.name = cap.caps_.browserName;
      browser.version = cap.caps_.version;
    } );
  } );

  it( 'should load the stylesheet', function() {
    var stylesheet = browser.baseUrl + '/static/css';

    if ( browser.name === 'internet explorer' && browser.version === '8' ) {
      stylesheet += '/main.ie.css';
    } else {
      stylesheet += '/main.css';
    }

    expect( browser.styleSheets ).toContain( stylesheet );
  } );

  it( 'should properly load in a browser', function() {
    expect( _sharedObject.header.isPresent() ).toBe( true );
  } );

  it( 'should include the logo', function() {
    expect( _sharedObject.logo.isPresent() ).toBe( true );
  } );

  it( 'should include navList', function() {
    expect( _sharedObject.navList.isPresent() ).toBe( true );
  } );

  it( 'should include four Primary Nav Links', function() {
    expect( _sharedObject.primaryLinks.count() ).toEqual( 6 );
  } );

  it( 'should include multiple Sub Nav Links', function() {
    expect( _sharedObject.subLinks.count() ).toBeGreaterThan( 1 );
  } );
} );
