'use strict';

var statePages = require(
  '../../page_objects/page_wagtail_states_pages.js' );
var SharedPage = statePages.sharedpage;
var SharedDraftPage = statePages.shareddraftpage;

var TITLE_TAGLINE = ' | Consumer Financial Protection Bureau';

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
