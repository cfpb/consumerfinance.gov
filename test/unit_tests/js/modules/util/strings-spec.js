const BASE_JS_PATH = '../../../../../cfgov/unprocessed/js/';
const strings = require( BASE_JS_PATH + 'modules/util/strings' );
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

describe( 'Strings stringValid()', () => {
  it( 'should return true when testing a standard string', () => {
    string = 'Test String';

    expect( strings.stringValid( string ) ).toBe( true );
  } );

  it( 'should return true when testing a hyphenated string', () => {
    string = 'Test-String';

    expect( strings.stringValid( string ) ).toBe( true );
  } );

  it( 'should return true when testing an underscored string', () => {
    string = 'Test_String';

    expect( strings.stringValid( string ) ).toBe( true );
  } );

  it( 'should return false when testing a string containing a single tick',
    () => {
      string = 'Person\'s Name';

      expect( strings.stringValid( string ) ).toBe( false );
    }
  );

  it( 'should return false when testing a string containing a period', () => {
    string = 'Some P. Name';

    expect( strings.stringValid( string ) ).toBe( false );
  } );

  it( 'should return false when testing a string containing a colon', () => {
    string = 'Person: Name';

    expect( strings.stringValid( string ) ).toBe( false );
  } );

  it( 'should return false when testing a string containing a gt or lt', () => {
    string = '<body>';

    expect( strings.stringValid( string ) ).toBe( false );
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
