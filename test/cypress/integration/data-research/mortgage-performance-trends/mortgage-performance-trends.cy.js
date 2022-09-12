import { MortgagePerformanceTrends } from './mortgage-performance-trends-helpers.cy.js';

const trends = new MortgagePerformanceTrends();

describe( 'Mortgage Performance Trends', () => {

  beforeEach( () => {
    trends.open();
    // preserve the cache. Deleting the cache but keeping the local files
    // between tests causes subsequent tests to fail.
    Cypress.Cookies.preserveOnce( 'sessionid' );
  } );

  it( 'should display delinquency trends chart for a given state', () => {
    trends.selectLocationType( 'State' );
    trends.selectStateForDelinquencyTrends( 'Virginia' );
    trends.highchartsLegendTitle().should( 'contain', 'Virginia');
  } );

  it( 'should display delinquency rates by month for a given state', () => {
    trends.selectStateForDelinquencyRatesPerMonth( 'Virginia' );
    trends.selectMonth( 'January' );
    trends.selectYear( '2017' );
    trends.mapTitle().should( 'contain', 'Virginia' );
    trends.mapTitle().should( 'contain', 'January' );
    trends.mapTitle().should( 'contain', '2017' );
  } );

} );
