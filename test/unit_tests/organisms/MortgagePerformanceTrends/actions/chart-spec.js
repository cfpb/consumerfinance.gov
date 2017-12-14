const BASE_JS_PATH = '../../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const mockery = require( 'mockery' );
const sinon = require( 'sinon' );
const expect = chai.expect;

// Disable the AJAX library used by the action creator
const noop = () => ( {} );
mockery.enable( {
  warnOnReplace: false,
  warnOnUnregistered: false
} );
mockery.registerMock( 'xdr', noop );

mockery.registerMock( '../utils', {
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
} );

const actions = require(
  BASE_JS_PATH + 'organisms/MortgagePerformanceTrends/actions/chart.js'
);

describe( 'Mortgage Performance chart action creators', () => {

  it( 'should dispatch actions to fetch metro states', () => {
    let dispatch = sinon.spy();
    actions.fetchMetroStates( 'AL', true )( dispatch );
    expect( dispatch.callCount ).to.equal( 2 );
    dispatch = sinon.spy();
    actions.fetchMetroStates( 'CA', true )( dispatch );
    expect( dispatch.callCount ).to.equal( 2 );
  } );

  it( 'should dispatch actions to fetch non-metro states', () => {
    const dispatch = sinon.spy();
    actions.fetchNonMetroStates( 'WY', true )( dispatch );
    expect( dispatch.callCount ).to.equal( 2 );
  } );

  it( 'should dispatch actions to fetch county states', () => {
    const dispatch = sinon.spy();
    actions.fetchCountyStates( 'CA', true )( dispatch );
    expect( dispatch.callCount ).to.equal( 2 );
  } );

  it( 'should dispatch actions to fetch states', () => {
    const dispatch = sinon.spy();
    actions.fetchStates( 'CA', true )( dispatch );
    expect( dispatch.callCount ).to.equal( 3 );
  } );

  it( 'should dispatch actions to fetch metros', () => {
    const dispatch = sinon.spy();
    actions.fetchMetros( 'AL', true )( dispatch );
    expect( dispatch.callCount ).to.equal( 4 );
    expect( actions.fetchMetros( 'AK', true ) ).to.throw();
  } );

  it( 'should fail on bad metro state abbr', () => {
    expect( actions.fetchMetros( 'bloop', true ) ).to.throw();
  } );

  it( 'should not require national data to be included with metros', () => {
    const dispatch = sinon.spy();
    actions.fetchMetros( 'AL', false )( dispatch );
    expect( dispatch.callCount ).to.equal( 4 );
  } );

  it( 'should dispatch actions to fetch counties', () => {
    const dispatch = sinon.spy();
    actions.fetchCounties( 'AL', true )( dispatch );
    expect( dispatch.callCount ).to.equal( 4 );
  } );

  it( 'should not require national data to be included with counties', () => {
    const dispatch = sinon.spy();
    actions.fetchCounties( 'AL', false )( dispatch );
    expect( dispatch.callCount ).to.equal( 4 );
  } );

  it( 'should fail on bad county state abbr', () => {
    expect( actions.fetchCounties( 'bloop', true ) ).to.throw();
  } );

} );
