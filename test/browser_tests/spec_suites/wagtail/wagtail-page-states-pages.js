'use strict';

var DraftPage = require(
  '../../page_objects/page_wagtail_states_pages.js' ).draftpage;
var SharedPage = require(
  '../../page_objects/page_wagtail_states_pages.js' ).sharedpage;
var LivePage = require(
  '../../page_objects/page_wagtail_states_pages.js' ).livepage;
var LiveDraftPage = require(
  '../../page_objects/page_wagtail_states_pages.js' ).livedraftpage;

describe( 'Wagtail Draft Page', function() {
  var page;

  beforeAll( function() {
    page = new DraftPage();
    page.get();
  } );

  it( 'should not load in a browser',
    function() {
      expect( 404 );
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
      expect( 404 );
    }
  );

  it( 'should properly load in a browser',
    function() {
      page.getStaging();
      expect( page.pageTitle() ).toContain(
        'Shared Page | Consumer Financial Protection Bureau' );
    }
  );

} );

describe( 'Wagtail Live Page', function() {
  var page;

  beforeAll( function() {
    page = new LivePage();
    page.get();
  } );

  it( 'should properly load in a browser',
    function() {
      expect( page.pageTitle() ).toContain(
        'Live Page | Consumer Financial Protection Bureau' );
    }
  );

} );

describe( 'Wagtail Live Draft Page', function() {
  var page;

  beforeAll( function() {
    page = new LiveDraftPage();
    page.get();
  } );

  it( 'should properly load in a browser',
    function() {
      expect( page.pageTitle() ).toContain(
        'Live Draft Page | Consumer Financial Protection Bureau' );
    }
  );

} );
