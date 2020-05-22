import * as strings from '../../../../../cfgov/unprocessed/js/modules/util/strings';
let string;
let control;

describe( 'Strings stringEscape()', () => {

  it( 'should escape a url', () => {
    string = 'https://google.com';

    expect( strings.stringEscape( string ) ).toBe( 'https://google\\.com' );
  } );

  it( 'should escape a hyphenated name', () => {
    string = 'Miller-Webster';

    expect( strings.stringEscape( string ) ).toBe( 'Miller\\-Webster' );
  } );

  it( 'should escape a comma', () => {
    string = 'Students, Parents, and Teachers';

    expect( strings.stringEscape( string ) )
      .toBe( 'Students, Parents, and Teachers' );
  } );
} );

describe( 'Strings stringMatch()', () => {
  it( 'should return true when testing matching strings', () => {
    string = 'Test String';
    control = 'Test String';

    expect( strings.stringMatch( control, string ) ).toBe( true );
  } );

  it( 'should return true when testing matching strings with differing casing',
    () => {
      string = 'test string';
      control = 'Test String';

      expect( strings.stringMatch( control, string ) ).toBe( true );
    }
  );

  it( 'should return false when testing differing strings', () => {
    string = 'Test String';
    control = 'Result String';

    expect( strings.stringMatch( control, string ) ).toBe( false );
  } );
} );
