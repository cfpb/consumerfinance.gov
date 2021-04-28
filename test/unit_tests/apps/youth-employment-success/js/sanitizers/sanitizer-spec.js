import {
  sanitizeMap
} from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/sanitizers';

describe( 'exposed sanitize functions', () => {
  describe( 'money', () => {
    const moneySanitizer = sanitizeMap['money'];

    it( 'strips all chars that are not numbers or a decimal', () => {
      const badMoney = 'aasdas12$2.3#';

      expect( moneySanitizer( badMoney ) ).toBe( '122.3' );
    } );

    it( 'does not allow for multiple zeros in a row at the beginning of the string', () => {
      expect( moneySanitizer( '00' ) ).toBe( '0' );
    } );

    it( 'allows for a 0 followed by a decimal point', () => {
      expect( moneySanitizer( '0.' ) ).toBe( '0.' );
    } );

    it( 'allows for a . at the beginning of the string', () => {
      expect( moneySanitizer( '.1' ) ).toBe( '.1' );
    } );

    it( 'only allows for a single decimal place', () => {
      const badMoney = '12.2.';
      expect( moneySanitizer( badMoney ) ).toBe( '12.2' );
      expect( moneySanitizer( '12..' ) ).toBe( '12.' );
    } );

    it( 'removes all leading zeros from a number', () => {
      expect( moneySanitizer( '000000100.11' ) ).toBe( '100.11' );
    } );

    it( 'truncates any numbers over a decimal precision of 2', () => {
      expect( moneySanitizer( '100.111' ) ).toBe( '100.11' );
    } );

    it( 'adds commas where appropriate', () => {
      expect( moneySanitizer( '1222' ) ).toBe( '1,222' );
      expect( moneySanitizer( '12222222.00' ) ).toBe( '12,222,222.00' );
      expect( moneySanitizer( '1@2222.0' ) ).toBe( '12,222.0' );
    } );
  } );

  describe( 'any other number', () => {
    const numberSanitizer = sanitizeMap['number'];

    it( 'strips all leading zeros', () => {
      expect( numberSanitizer( '000001' ) ).toBe( '1' );
    } );

    it( 'removes all characters that are not digits', () => {
      expect( numberSanitizer( '@#Fd,,/:jfsjdhs2d' ) ).toBe( '2' );
    } );
  } );
} );
