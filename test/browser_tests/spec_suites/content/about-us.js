'use strict';

var AboutUs = require(
    '../../page_objects/page_about-us.js'
  );

describe( 'About Landing Page', function() {
  var page;

  beforeAll( function() {
    page = new AboutUs();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'About us' );
  } );

  it( 'should load the activity block in the sidebar', function() {
    expect( page.activityBlock ).toExist;
  } );

  it( 'should have Blog & Newspaper section in the Activity feed', function() {
    expect( page.firstIcon.getAttribute( 'class' ) )
      .toContain( 'cf-icon cf-icon-speech-bubble' );

    expect( page.secondIcon.getAttribute( 'class' ) )
      .toContain( 'cf-icon cf-icon-newspaper' );
  } );

  it( 'should display some activity items in the activity block', function() {
    expect( page.activityItems ).toExist;
  } );
} );
