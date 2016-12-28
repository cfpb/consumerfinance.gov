'use strict';

var WorkingAtCFPB = require(
    '../../page_objects/page_careers-working-at-cfpb.js'
  );

var Urlmatcher = require( '../../util/url-matcher' );

describe( 'The Working At CFPB Page', function() {
  var page;

  beforeAll( function() {
    page = new WorkingAtCFPB();
    page.get();

    jasmine.addMatchers( Urlmatcher );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Working at the CFPB' );
  } );

  it( 'should have a sideNav', function() {
    expect( page.sideNav.isPresent() ).toBe( true );
  } );

  it( 'should have an intro title', function() {
    expect( page.introSectionTitle.getText() ).toBe( 'Working at the CFPB' );
  } );

  it( 'should have mobile carousel items ', function() {
    expect( page.mobileCarouselItems.count() ).toBeGreaterThan( 0 );
  } );

  it( 'should have a career info section', function() {
    var infoSectionTitles = [
      'Current openings', 'Job application process',
      'Students & recent graduates'
    ];
    var infoSectionLinks = [
      '/about-us/careers/current-openings/',
      '/about-us/careers/application-process/',
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

} );
