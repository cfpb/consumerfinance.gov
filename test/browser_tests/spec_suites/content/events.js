'use strict';

var events = require( '../../page_objects/page_events.js' );
var EventsPage = events.EventsPage;
var ArchivePage = events.ArchivePage;

describe( 'Events Landing page', function() {
  var googleAPI = 'https://maps.googleapis.com/maps/api/staticmap?';
  var page;

  beforeAll( function() {
    page = new EventsPage();
    page.get();
  } );

  xit( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Upcoming Events' );
  } );

  xit( 'should include a hero', function() {
    expect( page.heroElem.isPresent() ).toBe( true );
    expect( page.hero.maps.count() ).toEqual( 2 );
    expect( page.hero.maps.get( 0 ).getAttribute( 'style' ) )
      .toContain( googleAPI );
    expect( page.hero.maps.get( 1 ).getAttribute( 'style' ) )
      .toContain( googleAPI );
    expect( page.hero.heading.getText() ).toBeDefined();
    expect( page.hero.date.getText() ).toBeDefined();
    expect( page.hero.time.getText() ).toBeDefined();
  } );

  xit( 'should include at least one event', function() {
    expect( page.events.count() ).toBeGreaterThan( 0 );
  } );

  xit( 'should include all event meta data', function() {
    expect( page.first.map.getAttribute( 'src' ) ).toContain( googleAPI );
    expect( page.first.heading.getText() ).toBeDefined();
    expect( page.first.city.getText() ).toBeDefined();
    expect( page.first.state.getText() ).toBeDefined();
    expect( page.first.date.getText() ).toBeDefined();
    expect( page.first.time.getText() ).toBeDefined();
    expect( page.first.tags ).toBe( true );
  } );
} );


describe( 'Events Archive page', function() {
  var page;

  beforeEach( function() {
    page = new ArchivePage();
    page.get();
  } );

  xit( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Past Events' );
  } );

  xit( 'should include at least one event', function() {
    expect( page.events.count() ).toBeGreaterThan( 0 );
  } );

  xit( 'should include all event meta data', function() {
    expect( page.first.heading.getText() ).toBeDefined();
    expect( page.first.city.getText() ).toBeDefined();
    expect( page.first.state.getText() ).toBeDefined();
    expect( page.first.date.getText() ).toBeDefined();
    expect( page.first.time.getText() ).toBeDefined();
    expect( page.first.tags.isPresent() ).toBe( true );
  } );
} );
