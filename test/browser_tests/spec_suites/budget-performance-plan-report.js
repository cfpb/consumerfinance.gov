'use strict';

var BudgetPerformancePlanReport = require(
    '../page_objects/page_budget-performance-plan-report.js'
  );

describe( 'The Budget Performance Plan Report Page', function() {
  var page;

  beforeAll( function() {
    page = new BudgetPerformancePlanReport();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Annual Performance Plan and Report' );
  } );

  it( 'should load a side nav', function() {
    expect( page.sideNav.isPresent() ).toBe( true );
  } );

  it( 'should have a breadcrumb', function() {
    expect( page.breadcrumb.getText() ).toBe( 'Budget and Strategy' );
  } );

  it( 'should have a main title', function() {
    expect( page.mainTitle.getText() ).toBe( 'Performance Plan & Report' );
  } );

  it( 'should have multiple Performance Plans', function() {
    expect( page.performancePlanTitles.count() ).toBeGreaterThan( 0 );
    expect( page.performancePlanLinks.count() ).toBeGreaterThan( 0 );
    page.performancePlanLinks.getAttribute( 'href' )
    .then( function( values ) {
      expect( values.join().indexOf( '.pdf' ) > -1 ).toBe( true );
    } );
  } );

} );
