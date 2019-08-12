import money from '../../../../../cfgov/unprocessed/apps/youth-employment-success/js/money';

describe( 'money helpers', () => {
  it( 'truncates entries over 2 decimal places to 2', () => {
    expect( money.add( '1.355', '1.655' ) ).toEqual( 3 );
  } );

  it( 'treats invalid entries as zero', () => {
    expect( money.add( '1DE', 'null' ) ).toEqual( 1 );
  } );

  it( 'subtracts values', () => {
    expect( money.subtract( '100', '50' ) ).toEqual( 50 );
  } );
} );
