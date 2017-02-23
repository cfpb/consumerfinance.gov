'use strict';

var ApplicationProcess = require(
    '../../page_objects/page_careers-application-process.js'
  );

var Urlmatcher = require( '../../util/url-matcher' );

describe( 'The Application Process Page', function() {
  var page;

  beforeAll( function() {
    page = new ApplicationProcess();
    page.get();
    jasmine.addMatchers( Urlmatcher );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Job Application Process' );
  } );

  it( 'should have a sideNav', function() {
    expect( page.sideNav.isPresent() ).toBe( true );
  } );

  it( 'should have three job application interfaces ', function() {
    expect( page.jobApplicationsInterfaces.count() ).toEqual( 3 );
  } );

  it( 'should have an ethics link ', function() {
    expect( page.ethicsLink.isPresent() ).toBe( true );
  } );

  it( 'should have a career info section', function() {
    var infoSectionTitles = [
      'Current openings', 'Working at the CFPB',
      'Students & recent graduates'
    ];
    var infoSectionLinks = [
      '/about-us/careers/current-openings/',
      '/about-us/careers/working-at-cfpb/',
      '/about-us/careers/students-and-graduates/'
    ];

    expect( page.infoSectionTitles.getText() )
    .toEqual( infoSectionTitles );
    expect( page.infoSectionDescriptions.count() ).toEqual( 5 );
    expect( page.infoSectionLinks.getAttribute( 'href' ) )
    .toEqualUrl( infoSectionLinks );
  } );

  it( 'should have a Related Links section', function() {
    expect( page.relatedLinksSection.isPresent() ).toBe( true );
  } );

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
} );
