'use strict';

var PageWagtailTemplate =
  require( '../../page_objects/page_wagtail_templates.js' );
var TITLE_TAGLINE = ' | Consumer Financial Protection Bureau';

describe( 'Wagtail Landing Page', function() {
  var page;

  beforeAll( function() {
    page = new PageWagtailTemplate.Landing();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Landing Page' + TITLE_TAGLINE );
  } );
} );

describe( 'Wagtail SubLanding Page', function() {
  var page;

  beforeAll( function() {
    page = new PageWagtailTemplate.Sublanding();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Sublanding Page' + TITLE_TAGLINE );
  } );
} );

describe( 'Wagtail Browse Page', function() {
  var page;

  beforeAll( function() {
    page = new PageWagtailTemplate.Browse();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Browse Page' + TITLE_TAGLINE );
  } );

} );

describe( 'Wagtail Browse Filterable Page', function() {
  var page;

  beforeAll( function() {
    page = new PageWagtailTemplate.BrowseFilterable();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Browse Filterable Page' );
  } );
} );

describe( 'Wagtail Sublanding Filterable Page', function() {
  var page;

  beforeAll( function() {
    page = new PageWagtailTemplate.SublandingFilterable();
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
    page = new PageWagtailTemplate.EventArchive();
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
    page = new PageWagtailTemplate.Learn();
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
    page = new PageWagtailTemplate.Event();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toContain( 'Event Page' + TITLE_TAGLINE );
  } );
} );

describe( 'Wagtail Document Detail Page', function() {
  var page;

  beforeAll( function() {
    page = new PageWagtailTemplate.Docdetail();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() )
      .toContain( 'Document Detail Page' + TITLE_TAGLINE );
  } );
} );

describe( 'Wagtail Newsroom Landing Page', function() {
  var page;

  beforeAll( function() {
    page = new PageWagtailTemplate.NewsroomLanding();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() )
      .toContain( 'Newsroom Landing Page' + TITLE_TAGLINE );
  } );
} );

describe( 'Wagtail Newsroom Page', function() {
  var page;

  beforeAll( function() {
    page = new PageWagtailTemplate.Newsroom();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() )
      .toContain( 'Newsroom Page' + TITLE_TAGLINE );
  } );
} );

describe( 'Wagtail Legacy Newsroom Page', function() {
  var page;

  beforeAll( function() {
    page = new PageWagtailTemplate.LegacyNewsroom();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() )
      .toContain( 'Legacy Newsroom Page' + TITLE_TAGLINE );
  } );
} );

describe( 'Wagtail Blog Page', function() {
  var page;

  beforeAll( function() {
    page = new PageWagtailTemplate.Blog();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() )
      .toContain( 'Blog Page' + TITLE_TAGLINE );
  } );
} );

describe( 'Wagtail Legacy Blog Page', function() {
  var page;

  beforeAll( function() {
    page = new PageWagtailTemplate.LegacyBlog();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() )
      .toContain( 'Legacy Blog Page' + TITLE_TAGLINE );
  } );
} );

describe( 'Wagtail Activity Log Page', function() {
  var page;

  beforeAll( function() {
    page = new PageWagtailTemplate.ActivityLog();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() )
      .toContain( 'Activity Log Page' + TITLE_TAGLINE );
  } );
} );
