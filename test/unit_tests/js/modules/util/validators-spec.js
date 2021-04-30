import * as validators from '../../../../../cfgov/unprocessed/js/modules/util/validators.js';
import ERROR_MESSAGES from '../../../../../cfgov/unprocessed/js/config/error-messages-config.js';

let testField;
let returnedObject;
const validDates = [ '1/22/2017', '11/4/09', '3-31-20', '1-1-1900',
  '5/2018', '12/18', '05-2010', '1/17', '2016' ];

const invalidDates = [ '305-20-2018', '8//2018', '90', '4/20000' ];


describe( 'Validators', () => {
  describe( 'date field', () => {
    beforeEach( () => {
      testField = document.createElement( 'input' );
    } );

    it( 'should return an empty object for a valid date', () => {
      testField.value = '11/12/2007';
      returnedObject = validators.date( testField );

      expect( returnedObject ).toStrictEqual( {} );
    } );

    it( 'should return an error object for a malformed date', () => {
      testField.value = '11.12.2007';
      returnedObject = validators.date( testField );

      expect( returnedObject['date'] ).toBe( false );
      expect( returnedObject['msg'] ).toBe( ERROR_MESSAGES.DATE.INVALID );
    } );

    it( 'should allow correctly formatted dates', () => {
      for ( let i = 0, len = validDates.length; i < len; i++ ) {
        testField.value = validDates[i];
        returnedObject = validators.date( testField );
        expect( returnedObject ).toStrictEqual( {} );
      }
    } );

    it( 'should reject incorrectly formatted dates', () => {
      for ( let i = 0, len = invalidDates.length; i < len; i++ ) {
        testField.value = invalidDates[i];
        returnedObject = validators.date( testField );
        expect( returnedObject['date'] ).toBe( false );
        expect( returnedObject['msg'] ).toBe( ERROR_MESSAGES.DATE.INVALID );
      }
    } );

    it( 'should return an error object for a UTC date', () => {
      testField.value = new Date( 2007, 11, 12 );
      returnedObject = validators.date( testField );

      expect( returnedObject['date'] ).toBe( false );
      expect( returnedObject['msg'] ).toBe( ERROR_MESSAGES.DATE.INVALID );
    } );
  } );

  describe( 'email field', () => {
    beforeEach( () => {
      testField = document.createElement( 'input' );
    } );

    it( 'should return an empty object for a valid email', () => {
      testField.value = 'test@demo.com';
      returnedObject = validators.email( testField );

      expect( returnedObject ).toStrictEqual( {} );
    } );

    it( 'should return an error object for a missing domain', () => {
      testField.value = 'test';
      returnedObject = validators.email( testField );

      expect( returnedObject['email'] ).toBe( false );
      expect( returnedObject['msg'] ).toBe( ERROR_MESSAGES.EMAIL.INVALID );
    } );

    it( 'should return an error object for a missing user', () => {
      testField.value = '@demo.com';
      returnedObject = validators.email( testField );

      expect( returnedObject['email'] ).toBe( false );
      expect( returnedObject['msg'] ).toBe( ERROR_MESSAGES.EMAIL.INVALID );
    } );
  } );

  describe( 'empty field', () => {
    beforeEach( () => {
      testField = document.createElement( 'input' );
      testField.setAttribute( 'required', '' );
    } );

    it( 'should return an empty object for a filed field', () => {
      testField.value = 'testing';
      returnedObject = validators.empty( testField );

      expect( returnedObject ).toStrictEqual( {} );
    } );

    it( 'should return an error object for am empty field', () => {
      testField.value = '';
      returnedObject = validators.empty( testField );

      expect( returnedObject['required'] ).toBe( false );
      expect( returnedObject['msg'] ).toBe( ERROR_MESSAGES.FIELD.REQUIRED );
    } );
  } );

  describe( 'checkbox field', () => {
    beforeEach( () => {
      testField = document.createElement( 'label' );
      testField.setAttribute( 'name', 'test-checkboxes' );
      testField.setAttribute( 'data-required', '2' );
    } );

    it( 'should return an empty object ' +
        'when total checkboxes equals required total', () => {
      const fieldset = [
        document.createElement( 'input' ),
        document.createElement( 'input' )
      ];
      returnedObject = validators.checkbox( testField, null, fieldset );

      expect( returnedObject ).toStrictEqual( {} );
    } );

    it( 'should return an empty object ' +
        'when total checkboxes is more than required total', () => {
      const fieldset = [
        document.createElement( 'input' ),
        document.createElement( 'input' ),
        document.createElement( 'input' )
      ];
      returnedObject = validators.checkbox( testField, null, fieldset );

      expect( returnedObject ).toStrictEqual( {} );
    } );

    it( 'should return an error object ' +
         'when total checkboxes is less than required total', () => {
      const fieldset = [
        document.createElement( 'input' )
      ];
      returnedObject = validators.checkbox( testField, null, fieldset );

      expect( returnedObject['checkbox'] ).toBe( false );
      expect( returnedObject['msg'] )
        .toBe( ERROR_MESSAGES.CHECKBOX.REQUIRED.replace( '%s', '2' )
        );
    } );

    it( 'should return an empty object when required total is empty', () => {
      testField.removeAttribute( 'data-required' );
      const fieldset = [
        document.createElement( 'input' )
      ];
      returnedObject = validators.checkbox( testField, null, fieldset );

      expect( returnedObject ).toStrictEqual( {} );
    } );
  } );

  describe( 'radio field', () => {
    beforeEach( () => {
      testField = document.createElement( 'label' );
      testField.setAttribute( 'name', 'test-radios' );
      testField.setAttribute( 'data-required', '1' );
    } );

    it( 'should return an empty object ' +
        'when total radios equals required total', () => {
      const fieldset = [
        document.createElement( 'input' )
      ];
      returnedObject = validators.radio( testField, null, fieldset );

      expect( returnedObject ).toStrictEqual( {} );
    } );

    it( 'should return an empty object ' +
        'when total radios is more than required total', () => {
      const fieldset = [
        document.createElement( 'input' ),
        document.createElement( 'input' )
      ];
      returnedObject = validators.radio( testField, null, fieldset );

      expect( returnedObject ).toStrictEqual( {} );
    } );

    it( 'should return an error object ' +
        'when total checkboxes is less than required total', () => {
      const fieldset = [];
      returnedObject = validators.radio( testField, null, fieldset );

      expect( returnedObject['radio'] ).toBe( false );
      expect( returnedObject['msg'] )
        .toBe( ERROR_MESSAGES.CHECKBOX.REQUIRED.replace( '%s', '1' ) );
    } );

    it( 'should return an empty object ' +
        'when required total is empty', () => {
      testField.removeAttribute( 'data-required' );
      const fieldset = [
        document.createElement( 'input' )
      ];
      returnedObject = validators.radio( testField, null, fieldset );

      expect( returnedObject ).toStrictEqual( {} );
    } );
  } );
} );
