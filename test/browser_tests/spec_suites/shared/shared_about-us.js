'use strict';

var AboutUs = require(
    '../../page_objects/page_about-us.js'
  );

describe( 'About Landing Page', function() {
  var page;

  beforeEach( function() {
    page = new AboutUs();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'About Us' );
  } );

  it( 'should load items in the sidebar', function() {
    expect( page.sidebar ).toExist;
  } );

  it( 'should have Blog & Newspaper section in the Activity feed', function() {
    var firstIcon = page.feedIcons.first();
    var secondIcon = page.feedIcons.last();

    expect(
      firstIcon.getAttribute( 'class' )
    ).toMatch( 'cf-icon cf-icon-speech-bubble' );

    expect(
      secondIcon.getAttribute( 'class' )
    ).toContain( 'cf-icon cf-icon-newspaper' );

  } );

} );
