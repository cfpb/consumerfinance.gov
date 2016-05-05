'use strict';

var statePages = require(
  '../../page_objects/page_wagtail_states_pages.js' );
var SharedPage = statePages.sharedpage;
var SharedDraftPage = statePages.shareddraftpage;

var TITLE_TAGLINE = ' | Consumer Financial Protection Bureau';


describe( 'Wagtail Draft Page', function() {
  var page;

  beforeAll( function() {
    page = browser.get( '/draft-page/' );
  } );

  it( 'should not load in a browser',
    function() {
      expect( !page );
    }
  );

} );

describe( 'Wagtail Shared Page', function() {
  var page;

  beforeAll( function() {
    page = new SharedPage();
  } );

  it( 'should not load in a browser',
    function() {
      page.get();
      expect( !page );
    }
  );

  it( 'should properly load in a browser',
    function() {
      page.getStaging();
      expect( page.pageTitle() ).toEqual( 'Shared Page' + TITLE_TAGLINE );
    }
  );

} );

describe( 'Wagtail Shared Draft Page', function() {
  var page;

  beforeAll( function() {
    page = new SharedDraftPage();
  } );

  it( 'should not load in a browser',
    function() {
      page.get();
      expect( !page );
    }
  );

  it( 'should properly load in a browser',
    function() {
      page.getStaging();
      expect( page.pageTitle() ).toEqual( 'Shared Page' + TITLE_TAGLINE );
    }
  );

  it( 'should not display unshared content',
    function() {
      page.getStaging();
      expect( page.pageTitle() ).not.toEqual(
        'Shared Draft Page' + TITLE_TAGLINE );
    }
  );

} );

describe( 'Wagtail Live Page', function() {
  beforeAll( function() {
    browser.get( '/live-page/' );
  } );

  it( 'should properly load in a browser',
    function() {
      expect( browser.getTitle() ).toEqual( 'Live Page' + TITLE_TAGLINE );
    }
  );

} );

describe( 'Wagtail Live Draft Page', function() {
  beforeAll( function() {
    browser.get( '/live-draft-page/' );
  } );

  it( 'should properly load in a browser',
    function() {
      expect( browser.getTitle() ).toEqual(
        'Live Draft Page' + TITLE_TAGLINE );
    }
  );

} );
