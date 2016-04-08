'use strict';

var pageWagtailTemplate =
  require( '../../page_objects/page_wagtail_templates.js' );
var LandingPage = pageWagtailTemplate.landing;
var SubLandingPage = pageWagtailTemplate.sublanding;
var BrowsePage = pageWagtailTemplate.browse;
var BrowseFilterablePage = pageWagtailTemplate.browseFilterable;
var SublandingFilterablePage = pageWagtailTemplate.sublandingFilterable;
var EventArchivePage = pageWagtailTemplate.eventArchive;
var LearnPage = pageWagtailTemplate.learn;
var EventPage = pageWagtailTemplate.event;
var DocumentDetailPage = pageWagtailTemplate.docdetail;

var TITLE_TAGLINE = ' | Consumer Financial Protection Bureau';

describe( 'Wagtail Landing Page', function() {
  var page;

  beforeAll( function() {
    page = new LandingPage();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Landing Page' + TITLE_TAGLINE );
  } );
} );

describe( 'Wagtail SubLanding Page', function() {
  var page;

  beforeAll( function() {
    page = new SubLandingPage();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Sublanding Page' + TITLE_TAGLINE );
  } );
} );

describe( 'Wagtail Browse Page', function() {
  var page;

  beforeAll( function() {
    page = new BrowsePage();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Browse Page' + TITLE_TAGLINE );
  } );

} );

describe( 'Wagtail Browse Filterable Page', function() {
  var page;

  beforeAll( function() {
    page = new BrowseFilterablePage();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Browse Filterable Page' );
  } );
} );

describe( 'Wagtail Sublanding Filterable Page', function() {
  var page;

  beforeAll( function() {
    page = new SublandingFilterablePage();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() )
      .toContain( 'Sublanding Filterable Page' + TITLE_TAGLINE );
  } );
} );

describe( 'Wagtail Event Archive Page', function() {
  var page;

  beforeAll( function() {
    page = new EventArchivePage();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() )
      .toContain( 'Event Archive Page' + TITLE_TAGLINE );
  } );
} );

describe( 'Wagtail Learn Page', function() {
  var page;

  beforeAll( function() {
    page = new LearnPage();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() )
      .toContain( 'Learn Page' + TITLE_TAGLINE );
  } );
} );

describe( 'Wagtail Event Page', function() {
  var page;

  beforeAll( function() {
    page = new EventPage();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Event Page' + TITLE_TAGLINE );
  } );
} );

describe( 'Wagtail Document Detail Page', function() {
  var page;

  beforeAll( function() {
    page = new DocumentDetailPage();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() )
      .toContain( 'Document Detail Page' + TITLE_TAGLINE );
  } );
} );
