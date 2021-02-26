import
Store
  // eslint-disable-next-line max-len
  from '../../../../../../cfgov/unprocessed/js/organisms/MortgagePerformanceTrends/stores/store';
import
YesStore
  // eslint-disable-next-line max-len
  from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/store/yes-store';

describe( 'YesStore', () => {
  it( 'is an instance of Store', () => {
    const store = new YesStore( jest.fn() );

    expect( store instanceof Store ).toBe( true );
  } );
} );
