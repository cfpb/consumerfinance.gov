'use strict';

var TheBureauPage = require( '../../page_objects/page_the-bureau.js' );

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

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

  describe( '(Video Player)', function() {

    describe( 'on page load', function() {
      it( 'should be present', function() {
        expect( page.videoPlayer.isPresent() ).toBe( true );
      } );

      it( 'should show the image and not the video', function() {
        expect( page.videoPlayerImageContainer.isDisplayed() ).toBe( true );
        expect( page.videoPlayerVideoContainer.isDisplayed() ).toBe( false );
      } );
    } );

    describe( 'on play button click', function() {
      beforeEach( function() {
        page.videoPlayerPlayButton.isDisplayed().then(
        function( playButtonIsVisible ) {
          if ( playButtonIsVisible === false ) {
            page.videoPlayerCloseButton.click();
          }
          page.videoPlayerPlayButton.click();
        } );
      } );

      it( 'should show the video and not the image', function() {
        expect( page.videoPlayerVideoContainer.isDisplayed() ).toBe( true );
        expect( page.videoPlayerImageContainer.isDisplayed() ).toBe( false );
      } );

      it( 'should attach an iframe', function() {
        expect( page.getVideoPlayerIframe().isPresent() ).toBe( true );
      } );
    } );

    describe( 'on close button click', function() {
      beforeEach( function() {
        page.videoPlayerCloseButton.isDisplayed().then(
        function( closeButtonIsVisible ) {
          if ( closeButtonIsVisible === false ) {
            page.videoPlayerPlayButton.click();
          }
          page.videoPlayerCloseButton.click();
        } );
      } );

      it( 'should hide the video and show the image', function() {
        expect( page.videoPlayerImageContainer.isDisplayed() ).toBe( true );
        expect( page.videoPlayerVideoContainer.isDisplayed() ).toBe( false );
      } );
    } );

  } );

  if ( browser.params.windowWidth > breakpointsConfig.bpSM.min &&
       browser.params.windowWidth < breakpointsConfig.bpSM.max ) {
    describe( '(mobile)', function() {
      it( 'should show the show button', function() {
        expect( page.showButton.isDisplayed() ).toBe( true );
      } );

      it( 'should show the hide button after clicked', function() {
        page.expandableTarget.click();
        browser.wait( page.hideButton.isDisplayed() );

      } );
    } );
  }

} );
