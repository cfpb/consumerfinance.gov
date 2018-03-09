const chai = require( 'chai' );
const expect = chai.expect;
const sinon = require( 'sinon' );

/* Disable the AJAX library used by the action creator
   Unfortunately, we can't place path variables into import statements. */
import * as actions from '../../../../../../cfgov/unprocessed/js/organisms/MortgagePerformanceTrends/actions/map.js';
import * as utils from '../../../../../../cfgov/unprocessed/js/organisms/MortgagePerformanceTrends/utils';

jest.mock( 'xdr', () => jest.fn( () => ( { mock: 'data' } ) ) );
jest.mock( '../../../../../../cfgov/unprocessed/js/organisms/MortgagePerformanceTrends/utils', () => ( {
  getMetroData: cb => {
    const metros = {
      AL: {
        metros: [
          {
            valid: true,
            fips: '12345',
            name: 'Acme metro'
          }
        ]
      }
    };
    cb( metros );
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
  }
} ) );

describe( 'Mortgage Performance map action creators', () => {

  it( 'should create an action to update the chart', () => {
    const action = actions.updateChart( 123, 'Alabama', 'state' );
    expect( action ).to.deep.equal( {
      type: 'UPDATE_CHART',
      geo: {
        id: 123,
        name: 'Alabama',
        type: 'state'
      }
    } );
  } );

  it( 'should create an action without a geo type', () => {
    const action = actions.updateChart( 123, 'Alabama' );
    expect( action ).to.deep.equal( {
      type: 'UPDATE_CHART',
      geo: {
        id: 123,
        name: 'Alabama'
      }
    } );
  } );

  it( 'should create an action without a geoId', () => {
    const action = actions.updateChart( null, null );
    expect( action ).to.deep.equal( {
      type: 'UPDATE_CHART',
      geo: {
        id: null,
        name: null
      },
      counties: [],
      metros: []
    } );
  } );

  it( 'should dispatch actions to fetch metros', () => {
    const dispatch = sinon.spy();
    actions.fetchMetros( 'AL', true )( dispatch );
    expect( dispatch.callCount ).to.equal( 3 );
  } );

  it( 'should fail on bad metro state abbr', () => {
    expect( actions.fetchMetros( 'bloop', true ) ).to.throw();
  } );

  it( 'should not require map zoom after fetching metros', () => {
    const dispatch = sinon.spy();
    actions.fetchMetros( 'AL', false )( dispatch );
    expect( dispatch.callCount ).to.equal( 2 );
  } );

  it( 'should dispatch actions to fetch counties', () => {
    const dispatch = sinon.spy();
    actions.fetchCounties( 'AL', true )( dispatch );
    expect( dispatch.callCount ).to.equal( 3 );
  } );

  it( 'should not require map zoom after fetching counties', () => {
    const dispatch = sinon.spy();
    actions.fetchCounties( 'AL', false )( dispatch );
    expect( dispatch.callCount ).to.equal( 2 );
  } );

  it( 'should fail on bad county state abbr', () => {
    expect( actions.fetchCounties( 'bloop', true ) ).to.throw();
  } );

} );
