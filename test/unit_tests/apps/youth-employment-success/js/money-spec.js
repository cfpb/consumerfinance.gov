import money from '../../../../../unprocessed/apps/youth-employment-success/js/money';

describe( 'money helpers', () => {
  describe( '.toDollars', () => {
    it( 'converts string amounts to dollars', () => {
      expect( money.toDollars( '125.567' ) ).toEqual( 126 );
    } );

    it( 'converts numbers to string for proper matching', () => {
      expect( money.toDollars( 125.9999 ) ).toEqual( 126 );
    } );
  } );

  it( 'rounds calculation up to nearest whole number', () => {
    expect( money.add( '1.355', '1.655' ) ).toEqual( 4 );
  } );

  it( 'treats invalid entries as zero', () => {
    expect( money.add( '1DE', 'null' ) ).toEqual( 1 );
  } );

  it( 'subtracts values', () => {
    expect( money.subtract( '100', '50' ) ).toEqual( 50 );
  } );
} );
