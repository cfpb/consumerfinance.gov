import enforceRange from '../../../../../../cfgov/unprocessed/apps/retirement/js/utils/enforce-range.js';

describe( 'enforceRange...', function() {
  it( '...should enforce maximums', function() {
    expect( enforceRange( 15, 1, 10 ) ).toEqual( 10 );
    expect( enforceRange( 150, 1, 100 ) ).toEqual( 100 );
    expect( enforceRange( 4, 2, 3 ) ).toEqual( 3 );
  });

  it( '...should enforce minimums', function() {
    expect( enforceRange( 5, 10, 15 ) ).toEqual( 10 );
    expect( enforceRange( 3, 5, 100 ) ).toEqual( 5 );
    expect( enforceRange( 1, 2, 3 ) ).toEqual( 2 );
  });

  it( '...should allow numbers within the range', function() {
    expect( enforceRange( 5, 1, 10 ) ).toEqual( 5 );
    expect( enforceRange( 155, 100, 1000 ) ).toEqual( 155 );
    expect( enforceRange( 1, 1, 10 ) ).toEqual( 1 );
    expect( enforceRange( 10, 1, 10 ) ).toEqual( 10 );
  });

  it( '...should return false if min is greater than max', function() {
    expect( enforceRange( 15, 20, 10 ) ).toEqual( false );
  });

  it( '...should return false if types are mixed', function() {
    expect( enforceRange( 1, 'a', 'c' ) ).toEqual( false );
  });

  it( '...should work on strings', function() {
    expect( enforceRange( 'd', 'a', 'c' ) ).toEqual( 'c' );
    expect( enforceRange( 'cat', 'bar', 'foo' ) ).toEqual( 'cat' );
    expect( enforceRange( 'lion', 'bar', 'foo' ) ).toEqual( 'foo' );
  });
});
