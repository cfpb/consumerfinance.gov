'use strict';
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
        name: 'Acme metro'
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
  }
} );

const actions = require( BASE_JS_PATH + 'organisms/MortgagePerformanceTrends/actions/chart.js' );

describe( 'Mortgage Performance chart action creators', () => {

  it( 'should dispatch actions to fetch metros', () => {
    const dispatch = sinon.spy();
    actions.fetchMetros( 'AL', true )( dispatch );
    expect( dispatch.callCount ).to.equal( 4 );
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
