'use strict';


var BrowseFilterablePage = require(
  '../../page_objects/browse-filterable-page.js'
);
var SublandingFilterablePage = require(
  '../../page_objects/sublanding-filterable-page.js'
);
var { defineSupportCode } = require( 'cucumber' );
var { expect } = require( 'chai' );

var browseFilterablePage = new BrowseFilterablePage();
var sublandingFilterablePage = new SublandingFilterablePage();
var filterablePages = {
  browse:     browseFilterablePage,
  sublanding: sublandingFilterablePage
};
var selectedFilterablePage;
var UNDEFINED;


defineSupportCode( function( { Then, When, After } ) {

  After( function() {
    selectedFilterablePage = UNDEFINED;
  } );

  When( /I goto a (.*) filterable page/, function( pageType ) {
    selectedFilterablePage = filterablePages[pageType];
    filterablePages[pageType].gotoURL();
  } );

  When( /I do not select a filter/, function() {

    return browser.getCurrentUrl().then( function( url ) {
      expect( url ).not.to.contain( '?' );
    } );
  } );

  Then( /I should see the (first|last) page result, (.*)/,
    function( pagePosition, pageName ) {

      return selectedFilterablePage.getResultText( pagePosition )
             .then( function( resultText ) {
               expect( resultText ).to.contain( pageName );
             } );
    }
  );

  Then( /I should see (.*) page results/, function( numPageResults ) {

    return selectedFilterablePage.getResultsCount()
           .then( function( resultsCount ) {
             expect( resultsCount ).to.equal( numPageResults );
           } );
  } );

} );
