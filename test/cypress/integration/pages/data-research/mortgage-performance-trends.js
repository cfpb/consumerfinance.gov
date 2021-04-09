import { MortgagePerformanceTrends } from '../../../pages/data-research/mortgage-performance-trends';

const trends = new MortgagePerformanceTrends();

describe( 'Mortgage Performance Trends', () => {

  it( 'should display delinquency trends chart for a given state', () => {
    trends.open();
    trends.selectLocationType( 'State' );
    trends.selectStateForDelinquencyTrends( 'Virginia' );
  } );

  it( 'should display delinquency rates by month for a given state', () => {
    trends.open();
    trends.selectStateForDelinquencyRatesPerMonth( 'Virginia' );
    trends.selectMonth( 'January' );
    trends.selectYear( '2017' );
    trends.mapTitle().should( 'contain', 'Virginia' );
    trends.mapTitle().should( 'contain', 'January' );
    trends.mapTitle().should( 'contain', '2017' );
  } );

} );
