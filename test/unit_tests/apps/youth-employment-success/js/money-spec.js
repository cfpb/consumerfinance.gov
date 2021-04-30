import money from '../../../../../cfgov/unprocessed/apps/youth-employment-success/js/money.js';

describe( 'money helpers', () => {
  describe( '.toDollars', () => {
    it( 'returns a 0 if an invalid string is supplied', () => {
      expect( money.toDollars( '.' ) ).toEqual( 0 );
      expect( money.toDollars( 'foo' ) ).toEqual( 0 );
    } );

    it( 'converts string amounts to dollars', () => {
      expect( money.toDollars( '125.567' ) ).toEqual( 125.56 );
    } );

    it( 'converts numbers to string for proper matching', () => {
      expect( money.toDollars( 125.9999 ) ).toEqual( 125.99 );
    } );
  } );

  it( 'preserves decimals in calculations', () => {
    expect( money.add( '1.355', '1.655' ) ).toEqual( 3 );
  } );

  it( 'treats invalid entries as zero', () => {
    expect( money.add( '1DE', 'null' ) ).toEqual( 1 );
  } );

  it( 'subtracts values', () => {
    expect( money.subtract( '100', '50' ) ).toEqual( 50 );
    expect( money.subtract( '-50', '50' ) ).toEqual( -100 );
  } );
} );
