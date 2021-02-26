/* Disable the AJAX library used by the action creator
   Unfortunately, we can't place path variables into import statements. */
import actions from '../../../../../../cfgov/unprocessed/js/organisms/MortgagePerformanceTrends/actions/chart.js';

jest.mock( 'xdr', () => jest.fn( () => ( { mock: 'data' } ) ) );
jest.mock( '../../../../../../cfgov/unprocessed/js/organisms/' +
           'MortgagePerformanceTrends/utils', () => ( {
  getMetroData: cb => {
    const metros = {
      AL: {
        metros: [
          {
            valid: true,
            fips: '12345',
            name: 'Acme metro'
          },
          {
            valid: true,
            fips: '12-non',
            name: 'Acme non-metro'
          }
        ]
      }
    };
    cb( metros );
  },
  getNonMetroData: cb => {
    const nonMetros = [
      {
        valid: true,
        fips: '12345',
        name: 'Acme metro',
        abbr: 'AL'
      }
    ];
    cb( nonMetros );
  },
  getCountyData: cb => {
    const counties = {
      AL: {
        counties: [
          {
            valid: true,
            fips: '12345',
            name: 'Acme county'
          }
        ]
      }
    };
    cb( counties );
  },
  getStateData: cb => {
    const counties = {
      10: {
        AP: 'Del.',
        fips: '10',
        name: 'Delaware',
        abbr: 'DE'
      },
      11: {
        AP: 'D.C.',
        fips: '11',
        name: 'District of Columbia',
        abbr: 'DC'
      }
    };
    cb( counties );
  }
} ) );

describe( 'Mortgage Performance chart action creators', () => {

  it( 'should dispatch actions to fetch metro states', () => {
    let dispatch = jest.fn();
    actions.fetchMetroStates( 'AL', true )( dispatch );
    expect( dispatch ).toHaveBeenCalledTimes( 2 );
    dispatch = jest.fn();
    actions.fetchMetroStates( 'CA', true )( dispatch );
    expect( dispatch ).toHaveBeenCalledTimes( 2 );
  } );

  it( 'should dispatch actions to fetch non-metro states', () => {
    const dispatch = jest.fn();
    actions.fetchNonMetroStates( 'WY', true )( dispatch );
    expect( dispatch ).toHaveBeenCalledTimes( 2 );
  } );

  it( 'should dispatch actions to fetch county states', () => {
    const dispatch = jest.fn();
    actions.fetchCountyStates( 'CA', true )( dispatch );
    expect( dispatch ).toHaveBeenCalledTimes( 2 );
  } );

  it( 'should dispatch actions to fetch states', () => {
    const dispatch = jest.fn();
    actions.fetchStates( 'CA', true )( dispatch );
    expect( dispatch ).toHaveBeenCalledTimes( 3 );
  } );

  it( 'should dispatch actions to fetch metros', () => {
    const dispatch = jest.fn();
    actions.fetchMetros( 'AL', true )( dispatch );
    expect( dispatch ).toHaveBeenCalledTimes( 4 );
    expect( actions.fetchMetros( 'AK', true ) ).toThrow();
  } );

  it( 'should fail on bad metro state abbr', () => {
    expect( actions.fetchMetros( 'bloop', true ) ).toThrow();
  } );

  it( 'should not require national data to be included with metros', () => {
    const dispatch = jest.fn();
    actions.fetchMetros( 'AL', false )( dispatch );
    expect( dispatch ).toHaveBeenCalledTimes( 4 );
  } );

  it( 'should dispatch actions to fetch counties', () => {
    const dispatch = jest.fn();
    actions.fetchCounties( 'AL', true )( dispatch );
    expect( dispatch ).toHaveBeenCalledTimes( 4 );
  } );

  it( 'should not require national data to be included with counties', () => {
    const dispatch = jest.fn();
    actions.fetchCounties( 'AL', false )( dispatch );
    expect( dispatch ).toHaveBeenCalledTimes( 4 );
  } );

  it( 'should fail on bad county state abbr', () => {
    expect( actions.fetchCounties( 'bloop', true ) ).toThrow();
  } );

} );
