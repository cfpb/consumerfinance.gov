import numToMoney from '../../../../../../cfgov/unprocessed/apps/retirement/js/utils/num-to-money.js';

let UNDEFINED;

describe( 'numToMoney...', function() {
  it( '...turn 5000000 into $5,000,000', function() {
    expect( numToMoney( 5000000 ) ).toEqual( '$5,000,000' );
  } );

  it( '...should turn -5000000 into -$5,000,000', function() {
    expect( numToMoney( -5000000 ) ).toEqual( '-$5,000,000' );
  } );

  it( '...should turn _undefined_ into $0', function() {
    expect( numToMoney( UNDEFINED ) ).toEqual( '$0' );
  } );

  it( '...should turn _undefined_ into $0', function() {
    expect( numToMoney( UNDEFINED ) ).toEqual( '$0' );
  } );

  it( '...should turn OBJECT into $0', function() {
    expect( numToMoney( { testObject: true } ) ).toEqual( '$0' );
  } );

} );
