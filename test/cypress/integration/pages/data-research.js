import { DelinquentMortgage } from '../../pages/data-research/deliquent-mortgages';

const delinquentMortgage = new DelinquentMortgage();

describe( 'Data Research', () => {

  describe( 'Delinquent Mortgages', () => {

    it( 'should display delinquency trends chart for a given state', () => {
      delinquentMortgage.open();
      delinquentMortgage.selectLocationType( 'State' );
      delinquentMortgage.selectStateForDelinquencyTrends( 'Virginia' );
    } );

    it( 'should display delinquency rates by month for a given state', () => {
      delinquentMortgage.open();
      delinquentMortgage.selectStateForDelinquencyRatesPerMonth( 'Virginia' );
      delinquentMortgage.selectMonth( 'January' );
      delinquentMortgage.selectYear( '2017' );
      delinquentMortgage.mapTitle().should( 'contain', 'Virginia' );
      delinquentMortgage.mapTitle().should( 'contain', 'January' );
      delinquentMortgage.mapTitle().should( 'contain', '2017' );
    } );

  } );

} );
