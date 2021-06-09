import validDates from '../../../../../../cfgov/unprocessed/apps/retirement/js/utils/valid-dates.js';

describe( 'validDates...', function() {
  it( '...should enforce date range by month', function() {
    expect( validDates( 10, 36, 2015 )['concat'] ).toEqual( '10-31-2015' );
    expect( validDates( 10, 0, 2015 )['concat'] ).toEqual( '10-1-2015' );
    expect( validDates( 2, 31, 2015 )['concat'] ).toEqual( '2-28-2015' );
    expect( validDates( 4, 31, 2015 )['concat'] ).toEqual( '4-30-2015' );
    expect( validDates( 6, 31, 2015 )['concat'] ).toEqual( '6-30-2015' );
    expect( validDates( 9, 31, 2015 )['concat'] ).toEqual( '9-30-2015' );
  } );

  it( '...should enforce months between 1 and 12', function() {
    expect( validDates( 13, 31, 2015 )['concat'] ).toEqual( '12-31-2015' );
    expect( validDates( 0, 31, 2015 )['concat'] ).toEqual( '1-31-2015' );
  } );

  it( '...should change two-digit years to be 19XX', function() {
    expect( validDates( 13, 31, 55 )['concat'] ).toEqual( '12-31-1955' );
    expect( validDates( 0, 31, 0 )['concat'] ).toEqual( '1-31-1900' );
  } );

  it( '...should understand leap years', function() {
    expect( validDates( 2, 29, 2004 )['concat'] ).toEqual( '2-29-2004' );
    expect( validDates( 2, 29, 2003 )['concat'] ).toEqual( '2-28-2003' );
  } );
} );
