const { Then, When } = require( 'cucumber' );
const { expect } = require( 'chai' );


When( /I do not select a filter/, async function() {
  const url = await browser.getCurrentUrl();

  return expect( url ).not.to.contain( '?' );
} );

Then( 'I should not see filtered results', function() {
  const notification = element(
    by.css( '.o-filterable-list-controls .m-notification' )
  );

  return expect( notification ).to.not.contain( 'filtered results' );
} );
