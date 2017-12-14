const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;
const getBreakpointState =
  require( BASE_JS_PATH + 'modules/util/breakpoint-state.js' ).get;
const breakpointConfig =
  require( BASE_JS_PATH + 'config/breakpoints-config.js' );

let breakpointState;
let configKeys;

describe( 'getBreakpointState', () => {
  before( () => {
    this.jsdom = require( 'jsdom-global' )();
  } );

  after( () => this.jsdom() );

  beforeEach( () => {
    configKeys = Object.keys( breakpointConfig );
  } );

  it( 'should return an object with properties from config file', () => {
    const breakpointStatekeys =
      Object.keys( breakpointConfig ).map( key => {
        key.replace( 'is', '' );
        key.charAt( 0 ).toLowerCase() + key.slice( 1 );
        return key;
      } );

    breakpointState = getBreakpointState();

    expect( breakpointState instanceof Object ).to.be.true;
    expect( configKeys.sort().join() === breakpointStatekeys.sort().join() )
      .to.be.true;
  } );

  it( 'should return an object with one state property set to true', () => {
    let trueValueCount = 0;

    breakpointState = getBreakpointState();
    for ( const stateKey in breakpointState ) { // eslint-disable-line guard-for-in, no-inline-comments, max-len
      if ( breakpointState[stateKey] === true ) trueValueCount++;
    }

    expect( trueValueCount === 1 ).to.be.true;
  } );

  it( 'should set the correct state property when passed width', () => {
    let width;
    let breakpointStateKey;

    for ( const rangeKey in breakpointConfig ) { // eslint-disable-line guard-for-in, no-inline-comments, max-len
      width = breakpointConfig[rangeKey].max ||
              breakpointConfig[rangeKey].min;
      breakpointState = getBreakpointState( width );
      breakpointStateKey =
      'is' + rangeKey.charAt( 0 ).toUpperCase() + rangeKey.slice( 1 );

      expect( breakpointState[breakpointStateKey] ).to.be.true;
    }
  } );

} );
