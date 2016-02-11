'use strict';

var BudgetPerformancePlanReport = require(
    '../page_objects/page_budget-financial-report.js'
  );

describe( 'The Budget Financial Report Page', function() {
  var page;

  beforeAll( function() {
    page = new BudgetPerformancePlanReport();
    page.get();
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Financial Report & Update' );
  } );

  it( 'should load a side nav', function() {
    expect( page.sideNav.isPresent() ).toBe( true );
  } );

  it( 'should have a breadcrumb', function() {
    expect( page.breadcrumb.getText() ).toBe( 'Budget and Strategy' );
  } );

  it( 'should have a main title', function() {
    expect( page.mainTitle.getText() ).toBe( 'Financial Reports & Updates' );
  } );

  it( 'should have multiple Financial Reports', function() {
    expect( page.financialReportTitles.count() ).toBeGreaterThan( 0 );
    expect( page.financialReportLinks.count() ).toBeGreaterThan( 0 );
    page.financialReportLinks.getAttribute( 'href' )
    .then( function( values ) {
      expect( values.join().indexOf( '.pdf' ) > -1 ).toBe( true );
    } );
  } );

} );
