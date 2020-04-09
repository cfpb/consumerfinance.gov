import "core-js/stable";
import "regenerator-runtime/runtime";

const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/paying-for-college';

const constantsModel = require( `${ BASE_JS_PATH }/js/models/constants-model.js` ).constantsModel;
const expensesModel = require( `${ BASE_JS_PATH }/js/models/expenses-model.js` ).expensesModel;
const schoolModel = require( `${ BASE_JS_PATH }/js/models/school-model.js` ).schoolModel;
const stateModel = require( `${ BASE_JS_PATH }/js/models/state-model.js` ).stateModel;

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

describe( 'The constants model', () => {

	describe( 'init', () => {

		it( 'should get values via an API call', async () => {
      const xhr = window.XMLHttpRequest;
      const xhrMock = createXHRMock();
      window.XMLHttpRequest = jest.fn( () => xhrMock );
      
      const promise = constantsModel.init();

      xhrMock.responseText = JSON.stringify( {
        someInterestRate: .0123
      } );

      xhrMock.onreadystatechange(); 

      await promise
        .then( response => {
          expect( constantsModel.values.someInterestRate ).toEqual( .0123 );
        } );

      window.XMLHttpRequest = xhr;
    } );
	} );
} );


describe( 'The expenses model', () => {

  describe( 'setValue', () => {
    it( 'should set a value in the model', async () => {
      expensesModel.setValue( 'foo', 13 );
      expect( expensesModel.values.foo ).toBe( 13 );
    } );
  } );

  describe( '_getSalaryRange', () => {
    it( 'should return the correct salary range', () => {
      let test;

      test = expensesModel._getSalaryRange( 3000 );
      expect( test ).toBe( 'less_than_5000' );

      test = expensesModel._getSalaryRange( 75000 );
      expect( test ).toBe( '70000_or_more' );
    } );
  } );

} );
