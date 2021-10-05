const module = require(
  '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/obfuscation'
);

const testName = 'Iñtërnâtiô Nàlizætiøn';

// Regular expression to check formal correctness of new encoding
const encodingRe = /^==(?:[A-Za-z\d-_]{4})*?(?:[A-Za-z\d-_]{2}(?:==)?|[A-Za-z\d-_]{3}=?)?$/;

describe( 'obfuscation module', () => {
  it( 'can encode in URL, replacing hash', () => {
    const url = module.encodeNameInUrl( 'http://google.com/#foo', testName );
    expect( ( /#foo/ ).test( url ) ).toEqual( false );
    const encoded = url.match( /#(.*)/ )[1];
    expect( encodingRe.test( encoded ) ).toEqual( true );
  } );

  it( 'can decode legacy values', () => {
    const sets = [
      [ 'A', 'MjcuMXQuDg==' ],
      [ 'AB', 'Yy4xbHQuTU4=' ],
      [ 'ABC', 'ay4xZHR1LlVWVw==' ],
      [ 'ABCD', 'MWouMTZ3cXEudnV0cw==' ]
    ];
    sets.forEach( ( [ initials, encoded ] ) => {
      const url = `http://google.com/#${ encoded }`;
      const decoded = module.decodeNameFromUrl( url );
      expect( decoded ).toEqual( initials );
    } );
  } );

  it( 'can reject invalid legacy values inside bas64', () => {
    const value = window.btoa( 'invalid-contents' );
    const url = 'http://google.com/#' + value;
    expect( module.decodeNameFromUrl( url ) ).toBeNull();
  } );

  it( 'can decode the encoded URL', () => {
    const url = module.encodeNameInUrl( 'http://google.com/#foo', testName );
    const decoded = module.decodeNameFromUrl( url );
    expect( decoded ).toEqual( testName );
  } );

  it( 'obfuscates the name!', () => {
    const url = module.encodeNameInUrl( 'http://google.com/#foo', testName );
    expect( url.indexOf( testName ) ).toEqual( -1 );
  } );

  it( 'rejects simple modification of the encoding', () => {
    const url = module.encodeNameInUrl( 'http://google.com/#foo', testName );
    const m = url.match( /#(.*)+/ );
    const unaltered = `#${ m[1] }`;

    // Bad format
    const altered1 = `#${ '1' + m[1] }`;

    // Bad base64
    const altered2 = `#==..${ m[1] }`;

    // Valid Base64 but not repeated
    const altered3 = '#' + m[1].substr( 0, 4 ) + 'z' + m[1].substr( 6 );

    expect( module.decodeNameFromUrl( unaltered ) ).toEqual( testName );
    expect( module.decodeNameFromUrl( altered1 ) ).toBeNull();
    expect( module.decodeNameFromUrl( altered2 ) ).toBeNull();
    expect( module.decodeNameFromUrl( altered3 ) ).toBeNull();
  } );

  it( 'does not occasionally fail', () => {
    for ( let i = 0; i < 200; i++ ) {
      const url = module.encodeNameInUrl( 'http://google.com/', 'ABCD' );
      expect( module.decodeNameFromUrl( url ) ).toEqual( 'ABCD' );
    }
  } );

} );
