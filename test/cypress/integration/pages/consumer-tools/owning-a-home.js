import { ExploreRates } from '../../../pages/consumer-tools/owning-a-home/explore-rates';

const exploreRates = new ExploreRates();

describe( 'Owning a Home', () => {
  describe( 'Explore Rates', () => {
    it( 'Should load the interest rates graph when a state has changed', () => {
      exploreRates.open();
      exploreRates.selectState( 'Virginia' );
      exploreRates.graph().should( 'exist' );
    } );
  } );
} );
