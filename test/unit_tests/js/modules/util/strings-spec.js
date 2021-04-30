import {
  formatTimestamp,
  stringEscape,
  stringMatch
} from '../../../../../cfgov/unprocessed/js/modules/util/strings.js';
let string;
let control;

describe( 'Strings formatTimestamp()', () => {
  it( 'should convert 23 seconds into 00:23 timestamp', () => {
    const seconds = 23;
    expect( formatTimestamp( seconds ) ).toBe( '00:23' );
  } );

  it( 'should convert 160 seconds into 02:40 timestamp', () => {
    const seconds = 160;
    expect( formatTimestamp( seconds ) ).toBe( '02:40' );
  } );

  it( 'should convert 16001 seconds into 04:26:41 timestamp', () => {
    const seconds = 16001;
    expect( formatTimestamp( seconds ) ).toBe( '04:26:41' );
  } );
} );

describe( 'Strings stringEscape()', () => {
  it( 'should escape a url', () => {
    string = 'https://google.com';

    expect( stringEscape( string ) ).toBe( 'https://google\\.com' );
  } );

  it( 'should escape a hyphenated name', () => {
    string = 'Miller-Webster';

    expect( stringEscape( string ) ).toBe( 'Miller\\-Webster' );
  } );

  it( 'should escape a comma', () => {
    string = 'Students, Parents, and Teachers';

    expect( stringEscape( string ) )
      .toBe( 'Students, Parents, and Teachers' );
  } );
} );

describe( 'Strings stringMatch()', () => {
  it( 'should return true when testing matching strings', () => {
    string = 'Test String';
    control = 'Test String';

    expect( stringMatch( control, string ) ).toBe( true );
  } );

  it( 'should return true when testing matching strings with differing casing',
    () => {
      string = 'test string';
      control = 'Test String';

      expect( stringMatch( control, string ) ).toBe( true );
    }
  );

  it( 'should return false when testing differing strings', () => {
    string = 'Test String';
    control = 'Result String';

    expect( stringMatch( control, string ) ).toBe( false );
  } );
} );
