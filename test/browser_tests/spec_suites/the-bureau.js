'use strict';

var TheBureauPage = require( '../page_objects/page_the-bureau.js' );

var BASE_JS_PATH = '../../../cfgov/unprocessed/js/';

var breakpointsConfig =
  require( BASE_JS_PATH + 'config/breakpoints-config' );

describe( 'The Bureau Page', function() {
  var page;

  beforeAll( function() {
    page = new TheBureauPage();
    page.get();
  } );

  it( 'should properly load in a browser',
    function() {
      expect( page.pageTitle() ).toContain( 'The Bureau' );
    }
  );

  it( 'should have a secondary nav',
    function() {
      expect( page.secondaryNav.isPresent() ).toBe( true );
    }
  );

  if ( browser.params.windowWidth > breakpointsConfig.bpSM.min &&
       browser.params.windowWidth < breakpointsConfig.bpSM.max ) {
    describe( '(mobile)', function() {
      it( 'should show the show button', function() {
        expect( page.showButton.isDisplayed() ).toBe( true );
      } );

      it( 'should show the hide button after clicked', function() {
        page.expandableTarget.click();
        page.wait( function() {
          return expect( page.hideButton.isDisplayed() ).toBe( true );
        }, 1000 );

      } );
    } );
  }

} );
