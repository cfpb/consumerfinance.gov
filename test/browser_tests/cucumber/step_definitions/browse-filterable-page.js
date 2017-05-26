'use strict';


var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var BrowseFilterablePage = require( '../../page_objects/browse-filterable-page.js' );
var browseFilterablePage = new BrowseFilterablePage();

var {defineSupportCode} = require('cucumber');
var {expect} = require('chai');

defineSupportCode( function( { Then, When } ) {
  When( 'I goto a browse filterable page', function() {
    browseFilterablePage.gotoURL();
  });

  When( 'I do not select a filter on the browse filterable page', function() {
    return browser.getCurrentUrl().then( function( url ) {
      expect( url ).not.to.contain( '?' )
    } )
  });

  Then ('I should see the first result, bfp child 0', function() {
    return browseFilterablePage.first_result.getText().then( function( first ) {
      expect(first).to.contain( 'bfp child 0' );
    })
  });

  Then ('I should see the last result, bfp child 9', function() {
    return browseFilterablePage.last_result.getText().then( function( last ) {
      expect(last).to.contain( 'bfp child 9' );
    })
  });

  Then ('I should see the right number of results on the browse filterable page', function() {
    return browseFilterablePage.results.count().then( function( num ) {
      expect( num ).to.equal( 10 );
    })
  })
});
