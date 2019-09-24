import Store from '../../../../../unprocessed/js/organisms/MortgagePerformanceTrends/stores/store';
import YesStore from '../../../../../unprocessed/apps/youth-employment-success/js/yes-store';

describe( 'YesStore', () => {
  it( 'is an instance of Store', () => {
    const store = new YesStore( jest.fn() );

    expect( store instanceof Store ).toBe( true );
  } );
} );
