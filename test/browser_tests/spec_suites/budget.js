'use strict';

var Budget = require(
    '../page_objects/page_budget.js'
  );

var Urlmatcher = require( '../util/url-matcher' );

describe( 'The Budget Page', function() {
  var page;

  beforeAll( function() {
    page = new Budget();
    page.get();

    jasmine.addMatchers( Urlmatcher );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Budget and Strategy' );
  } );

  it( 'should load a side nav', function() {
    expect( page.sideNav.isPresent() ).toBe( true );
  } );

  it( 'should have a mission summary', function() {
    expect( page.missionSummary.isPresent() ).toBe( true );
  } );

  it( 'should more than one mission statements', function() {
    expect( page.missionStatements.count() ).toBeGreaterThan( 1 );
  } );

  it( 'should have Budget sections', function() {
    var budgetSectionTitles =
    [ 'Strategic plan', 'Performance plans and reports',
    'Financial reports and updates', 'Funding requests' ];
    var budgetSectionLinks =
    [ '/budget/strategic-plan/', '/budget/performance-plan-report/',
    '/budget/financial-report/', '/budget/funding-request/' ];

    expect( page.budgetSectionTitles.getText() )
    .toEqual( budgetSectionTitles );
    expect( page.budgetSectionDescriptions.count() ).toEqual( 4 );
    expect( page.budgetSectionLinks.getAttribute( 'href' ) )
    .toEqualUrl( budgetSectionLinks );
  } );

  it( 'should have a Business With CFPB section', function() {
    var budgetSectionLinks = [ '/the-bureau/',
                               '/blog/',
                               '/sub-pages/civil-penalty-fund/' ];

    expect( page.relatedLinksTitle.getText() )
    .toBe( 'RELATED LINKS' );
    expect( page.relatedLinks.getAttribute( 'href' ) )
    .toEqualUrl( budgetSectionLinks );
  } );

} );
