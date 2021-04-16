const BrowseFilterablePage = require(
  '../../page_objects/browse-filterable-page.js'
);
const SublandingFilterablePage = require(
  '../../page_objects/sublanding-filterable-page.js'
);
const { Then, When, After } = require( '@cucumber/cucumber' );
const { expect } = require( 'chai' );

const browseFilterablePage = new BrowseFilterablePage();
const sublandingFilterablePage = new SublandingFilterablePage();
const filterablePages = {
  browse:     browseFilterablePage,
  sublanding: sublandingFilterablePage
};
let selectedFilterablePage;
let UNDEFINED;


After( function() {
  selectedFilterablePage = UNDEFINED;
} );

When( /I goto a (.*) filterable page/, function( pageType ) {
  selectedFilterablePage = filterablePages[pageType];

  return filterablePages[pageType].gotoURL();
} );

When( /I do not select a filter/, async function() {
  const url = await browser.getCurrentUrl();

  return expect( url ).not.to.contain( '?' );
} );

Then( /I should see the (first|last) page result, (.*)/,
  async function( pagePosition, pageName ) {
    const resultText =
      await selectedFilterablePage.getResultText( pagePosition );

    return expect( resultText ).to.contain( pageName );
  }
);

Then( /I should see (.*) page results/,
  async function( numPageResults ) {
    const resultsCount = await selectedFilterablePage.getResultsCount();

    return expect( resultsCount ).to.equal( numPageResults );
  }
);

Then( 'I should not see filtered results', function() {
  () => element( by.css( '.o-filterable-list-controls .m-notification' ) )
    .isDisplayed().then( displayed => expect( displayed ).to.be.false );
} );
