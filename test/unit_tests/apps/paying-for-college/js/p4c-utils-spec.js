// const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/paying-for-college';

// const stringToNum = require( `${ BASE_JS_PATH }/js/util/number-utils.js` ).stringToNum;

import "core-js/stable";
import "regenerator-runtime/runtime";
import { decimalToPercentString } from '../../../../../cfgov/unprocessed/apps/paying-for-college/js/util/number-utils'
import { stringToNum } from '../../../../../cfgov/unprocessed/apps/paying-for-college/js/util/number-utils'
import { promiseRequest } from '../../../../../cfgov/unprocessed/apps/paying-for-college/js/util/promise-request'

const createXHRMock = data => {
  const xhrMock = {
    open: jest.fn(),
    send: jest.fn(),
    readyState: 4,
    status: 200,
    responseText: JSON.stringify( data || {})
  };
  return xhrMock;
};

describe( 'The number utility stringToNum', () => {

  it( 'should convert strings to raw numbers', () => {
    expect( stringToNum( 'foo5' ) ).toEqual( 5 );
    expect( stringToNum( '13a' ) ).toEqual( 13 );
    expect( stringToNum( 'aaa' ) ).toEqual( 0 );
    expect( stringToNum( '-7' ) ).toEqual( -7 );
    expect( stringToNum( undefined ) ).toEqual( 0 );
    expect( stringToNum( { foo: 'bar' } ) ).toEqual( 0 );
    expect( stringToNum( '33.3.3' ) ).toEqual( 33.33 );
  } );

} );

describe( 'The number utility decimalToPercentString', () => {

  it( 'should convert decimals to percentage strings', () => {
    expect( decimalToPercentString( .55, 0 ) ).toEqual( '55%' );
    expect( decimalToPercentString( .0133, 2 ) ).toEqual( '1.33%' );
    expect( decimalToPercentString( 0, 0 ) ).toEqual( '0%' );
  } );

} );

describe( 'The XHR utility promiseRequest', () => {

  const xhr = global.XMLHttpRequest;
  let xhrMock;

  beforeEach( () => {
    xhrMock = createXHRMock();
    window.XMLHttpRequest = jest.fn( () => xhrMock );
  } );

  afterEach( () => {
    window.XMLHttpRequest = xhr;
  } );

  it( 'should create a Promise for an XHR', async () => {
    const promise = promiseRequest( 'GET', '/foo/' );
    xhrMock.responseText = JSON.stringify( {
      foo: 'bar'
    } );

    xhrMock.onreadystatechange(); 

    await promise
      .then( response => {
        const data = JSON.parse( response.responseText );
        expect( xhrMock.open ).toBeCalledWith( 'GET',  '/foo/', true );
        expect( data.foo ).toEqual( 'bar' );
      } );
  } );


} );
