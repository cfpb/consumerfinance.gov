import handleStringInput from '../../../../../../cfgov/unprocessed/apps/retirement/js/utils/handle-string-input.js';

describe( 'handleStringInput...', function() {

  it( '...will parse number strings with non-numeric characters', function() {
    expect( handleStringInput( '9a99' ) ).toEqual( 999 );
    expect( handleStringInput( 'u123456' ) ).toEqual( 123456 );
    expect( handleStringInput( '01234' ) ).toEqual( 1234 );
    expect( handleStringInput( '$1,234,567' ) ).toEqual( 1234567 );
    expect( handleStringInput( 'Ilikethenumber5' ) ).toEqual( 5 );
    expect( handleStringInput( 'function somefunction() { do badstuff; }' ) ).toEqual( 0 );
  } );

  it( '...will parse the first period as a decimal point', function() {
    expect( handleStringInput( '4.22' ) ).toEqual( 4.22 );
    expect( handleStringInput( 'I.like.the.number.5' ) ).toEqual( 0.5 );
    expect( handleStringInput( '1.2.3.4.5.6.7' ) ).toEqual( 1.234567 );
  } );

} );
