const BrowseFilterablePage = require(
  '../../page_objects/browse-filterable-page.js'
);
const SublandingFilterablePage = require(
  '../../page_objects/sublanding-filterable-page.js'
);
const { defineSupportCode } = require( 'cucumber' );
const { expect } = require( 'chai' );

const browseFilterablePage = new BrowseFilterablePage();
const sublandingFilterablePage = new SublandingFilterablePage();
const filterablePages = {
  browse:     browseFilterablePage,
  sublanding: sublandingFilterablePage
};
let selectedFilterablePage;
let UNDEFINED;


defineSupportCode( function( { Then, When, After } ) {

  After( function() {
    selectedFilterablePage = UNDEFINED;
  } );

  When( /I goto a (.*) filterable page/, function( pageType ) {
    selectedFilterablePage = filterablePages[pageType];

    return filterablePages[pageType].gotoURL();
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
