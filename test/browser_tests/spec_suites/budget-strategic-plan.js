'use strict';

var BudgetStrategicPlan = require(
    '../page_objects/page_budget-strategic-plan.js'
  );

var Urlmatcher = require( '../util/url-matcher' );

describe( 'The Budget Strategic Plan Page', function() {
  var page;

  beforeAll( function() {
    page = new BudgetStrategicPlan();
    page.get();

    jasmine.addMatchers( Urlmatcher );
  } );

  it( 'should properly load in a browser', function() {
    expect( page.pageTitle() ).toBe( 'Strategic Plan' );
  } );

  it( 'should have a side nav', function() {
    expect( page.sideNav.isPresent() ).toBe( true );
  } );

  it( 'should have a breadcrumb', function() {
    expect( page.breadcrumb.getText() ).toBe( 'Budget and Strategy' );
  } );

  it( 'should have a main title', function() {
    expect( page.mainTitle.getText() ).toBe( 'Strategic Plan' );
  } );

  it( 'should have a sub title', function() {
    expect( page.mainSubTitle.getText() ).toBe( 'CFPB Strategic Plan' );
  } );

  it( 'should have multiple main links', function() {
    var mainLinks =
    [ '/budget/strategic-plan/interactive/',
    'http://files.consumerfinance.gov/f/strategic-plan.pdf' ];

    expect( page.mainLinks.getAttribute( 'href' ) )
    .toEqualUrl( mainLinks );
  } );

} );
