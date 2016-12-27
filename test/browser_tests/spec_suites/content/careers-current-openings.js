'use strict';

var CurrentOpenings = require(
    '../../page_objects/page_careers-current-openings.js'
  );

var Urlmatcher = require( '../../util/url-matcher' );

describe( 'The Current Openings Page', function() {
  var page;

  beforeAll( function() {
    page = new CurrentOpenings();
    page.get();

    jasmine.addMatchers( Urlmatcher );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Current Openings' );
  } );

  it( 'should have a sideNav', function() {
    expect( page.sideNav.isPresent() ).toBe( true );
  } );

  it( 'should have a career info section', function() {
    var infoSectionTitles = [
      'Job application process',
      'Working at the CFPB'
    ];
    var infoSectionLinks = [
      '/about-us/careers/application-process/',
      '/about-us/careers/working-at-cfpb/'
    ];

    expect( page.infoSectionTitles.getText() )
    .toEqual( infoSectionTitles );
    expect( page.infoSectionDescriptions.count() ).toEqual( 4 );
    expect( page.infoSectionLinks.getAttribute( 'href' ) )
    .toEqualUrl( infoSectionLinks );
  } );

  it( 'should have a Related Links section', function() {
    expect( page.relatedLinksSection.isPresent() ).toBe( true );
  } );

} );
