import { decodeNameFromUrl } from '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/encode-name';

const module = require(
  '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/encode-name.js'
);

const testName = 'Iñtërnâtiô Nàlizætiøn';

// Regular expression to check formal correctness of base64 encoded strings
const b64re = /^(?:[A-Za-z\d+/]{4})*?(?:[A-Za-z\d+/]{2}(?:==)?|[A-Za-z\d+/]{3}=?)?$/;

describe( 'encode-name module', () => {

  beforeEach( () => {
    jest.spyOn( global.Math, 'random' ).mockReturnValue( 0.123 );
  } );

  afterEach( () => {
    jest.spyOn( global.Math, 'random' ).mockRestore();
  } );

  it( 'can encode in URL, replacing hash', () => {
    const url = module.encodeNameInUrl( 'http://google.com/#foo', testName );
    expect( ( /#foo/ ).test( url ) ).toEqual( false );
    const encoded = url.match( /#(.*)/ )[1];
    expect( b64re.test( encoded ) ).toEqual( true );
  } );

  it( 'can decode the encoded URL', () => {
    const url = module.encodeNameInUrl( 'http://google.com/#foo', testName );
    const decoded = module.decodeNameFromUrl( url );
    expect( decoded ).toEqual( testName );
  } );

  it( 'encodes with random', () => {
    const out1 = module.encodeNameInUrl( '', testName );
    jest.spyOn( global.Math, 'random' ).mockReturnValue( 0.79 );
    const out2 = module.encodeNameInUrl( '', testName );

    expect( out1 ).toEqual( '#ZC45NW14dTYuRPx55n9j73lk+S1D7WFkd+t5ZPVj' );
    expect( out2 ).toEqual( '#MjcuOTVteHU2Lga+O6Q9Ia07JrtvAa8jJjWpOya3IQ==' );
  } );

  it( 'obfuscates the name!', () => {
    const url = module.encodeNameInUrl( 'http://google.com/#foo', testName );
    expect( url.indexOf( testName ) ).toEqual( -1 );
  } );

  it( 'rejects modification of the encoding', () => {
    const url = module.encodeNameInUrl( 'http://google.com/#foo', testName );
    const m = url.match( /#(.*)+/ );
    const unaltered = `#${ m[1] }`;
    const altered1 = `#${ '1' + m[1] }`;

    expect( decodeNameFromUrl( unaltered ) ).toEqual( testName );
    expect( decodeNameFromUrl( altered1 ) ).toBeNull();
  } );

} );
