'use strict';

var Careers = require(
    '../../page_objects/page_careers.js'
  );

var Urlmatcher = require( '../../util/url-matcher' );

describe( 'The Careers Page', function() {
  var page;

  beforeAll( function() {
    page = new Careers();
    page.get();

    jasmine.addMatchers( Urlmatcher );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Careers at the CFPB' );
  } );

  it( 'should have an openings section', function() {
    expect( page.openingsSection.isPresent() ).toBe( true );
  } );

  it( 'should have a content sidebar', function() {
    expect( page.contentSidebar.isPresent() ).toBe( true );
  } );

  it( 'should have a career info section', function() {
    var infoSectionTitles = [
      'Job application process',
      'Students and recent graduates'
    ];
    var infoSectionLinks = [
      '/about-us/careers/application-process/',
      '/about-us/careers/students-and-graduates/'
    ];

    expect( page.infoSectionTitles.getText() )
    .toEqual( infoSectionTitles );
    expect( page.infoSectionDescriptions.count() ).toEqual( 2 );
    expect( page.infoSectionLinks.getAttribute( 'href' ) )
    .toEqualUrl( infoSectionLinks );
  } );

} );
