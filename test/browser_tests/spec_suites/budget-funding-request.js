'use strict';

var BudgetFundingRequest = require(
    '../page_objects/page_budget-funding-request.js'
  );

describe( 'The Budget Funding Request Page', function() {
  var page;

  beforeAll( function() {
    page = new BudgetFundingRequest();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Funding Requests' );
  } );

  it( 'should load a side nav', function() {
    expect( page.sideNav.isPresent() ).toBe( true );
  } );

  it( 'should have a breadcrumb', function() {
    expect( page.breadcrumb.getText() ).toBe( 'Budget and Strategy' );
  } );

  it( 'should have a main title', function() {
    expect( page.mainTitle.getText() ).toBe( 'Funding Requests' );
  } );

  it( 'should have multiple Funding Requests', function() {
    expect( page.fundingRequestTitles.count() ).toBeGreaterThan( 0 );
    expect( page.fundingRequestLinks.count() ).toBeGreaterThan( 0 );
    page.fundingRequestLinks.getAttribute( 'href' )
    .then( function( values ) {
      expect( values.join().indexOf( '.pdf' ) > -1 ).toBe( true );
    } );
  } );

} );
