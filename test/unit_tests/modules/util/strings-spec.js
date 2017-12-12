const chai = require( 'chai' );
const expect = chai.expect;
const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const strings = require( BASE_JS_PATH + 'modules/util/strings' );
let string;
let control;

describe( 'Strings stringEscape()', () => {

  it( 'should escape a url', () => {
    string = 'http://google.com';

    expect( strings.stringEscape( string ) )
      .to.equal( 'http://google\\.com' );
  } );

  it( 'should escape a hyphenated name', () => {
    string = 'Miller-Webster';

    expect( strings.stringEscape( string ) )
      .to.equal( 'Miller\\-Webster' );
  } );

  it( 'should escape a comma', () => {
    string = 'Students, Parents, and Teachers';

    expect( strings.stringEscape( string ) )
      .to.equal( 'Students, Parents, and Teachers' );
  } );
} );

describe( 'Strings stringValid()', () => {
  it( 'should return true when testing a standard string', () => {
    string = 'Test String';

    expect( strings.stringValid( string ) ).to.be.true;
  } );

  it( 'should return true when testing a hyphenated string', () => {
    string = 'Test-String';

    expect( strings.stringValid( string ) ).to.be.true;
  } );

  it( 'should return true when testing an underscored string', () => {
    string = 'Test_String';

    expect( strings.stringValid( string ) ).to.be.true;
  } );

  it( 'should return false when testing a string containing a single tick',
    () => {
      string = 'Person\'s Name';

      expect( strings.stringValid( string ) ).to.be.false;
    }
  );

  it( 'should return false when testing a string containing a period', () => {
    string = 'Some P. Name';

    expect( strings.stringValid( string ) ).to.be.false;
  } );

  it( 'should return false when testing a string containing a colon', () => {
    string = 'Person: Name';

    expect( strings.stringValid( string ) ).to.be.false;
  } );

  it( 'should return false when testing a string containing a gt or lt', () => {
    string = '<body>';

    expect( strings.stringValid( string ) ).to.be.false;
  } );
} );

describe( 'Strings stringMatch()', () => {
  it( 'should return true when testing matching strings', () => {
    string = 'Test String';
    control = 'Test String';

    expect( strings.stringMatch( control, string ) )
      .to.be.true;
  } );

  it( 'should return true when testing matching strings with differing casing',
    () => {
      string = 'test string';
      control = 'Test String';

      expect( strings.stringMatch( control, string ) )
        .to.be.true;
    }
  );

  it( 'should return false when testing differing strings', () => {
    string = 'Test String';
    control = 'Result String';

    expect( strings.stringMatch( control, string ) )
      .to.be.false;
  } );
} );
