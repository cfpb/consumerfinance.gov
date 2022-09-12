import { MortgagePerformanceTrends } from './mortgage-performance-trends-helpers.cy.js';

const trends = new MortgagePerformanceTrends();

describe( 'Mortgage Performance Trends', () => {

  beforeEach( () => {
    trends.open();
  } );

  it( 'should display delinquency trends chart for a given state', () => {
    trends.selectLocationType( 'State' );
    trends.selectStateForDelinquencyTrends( 'Virginia' );
    trends.highchartsLegendTitle().should( 'contain', 'Virginia');
    trends.clearStorage();
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
