/**
 * Obfuscate a string with simple Base64URL encoding
 */

const base64UrlEncode = val => window.btoa( val )
  .replace( /\+/g, '-' )
  .replace( /\//g, '_' );
const base64UrlDecode = val => window.atob(
  val
    .replace( /-/g, '+' )
    .replace( /_/g, '/' )
);

/**
 * Encode string
 *
 * @param {string} input Input
 * @returns {string} Encoded string
 */
function encode( input ) {
  const enc = base64UrlEncode;
  return '==' + enc( enc( enc( enc( input ) ) ) );
}

/**
 * Decode a string
 *
 * @param {string} encoded Encoded string
 * @returns {string | null} Decoded string (or null)
 */
function decode( encoded ) {
  if ( encoded.indexOf( '==' ) !== 0 ) {
    return legacyDecode( encoded );
  }

  // Trim leading "=="
  let value = encoded.substr( 2 );

  try {
    const dec = base64UrlDecode;
    return dec( dec( dec( dec( value ) ) ) );
  } catch ( err ) {
    return null;
  }
}

/**
 * Encode name as a URL hash
 *
 * @param {string} url URL
 * @param {string} name Name
 * @returns {string} Output URL
 */
function encodeNameInUrl( url, name ) {
  return url.replace( /#.*/, '' ) + '#' + encode( name );
}

/**
 * Decode name from a URL
 *
 * @param {string} url URL
 * @returns {string | null} Name, if set and valid
 */
function decodeNameFromUrl( url ) {
  return decode( url.replace( /^[^#]*#/, '' ) );
}

/**
 * Decode a string with legacy strategy
 *
 * @param {string} encoded Encoded string
 * @returns {string | null} Decoded string (or null)
 */
function legacyDecode( encoded ) {
  /**
   * Create a hash code for a string
   *
   * Adapted from https://stackoverflow.com/a/7616484/3779
   *
   * @param {string} str String to hash
   * @returns {string} Hash code
   */
  function hashCode( str ) {
    let hash = 0;
    for ( let i = 0; i < str.length; i++ ) {
      const chr = str.charCodeAt( i );
      hash = ( ( hash << 5 ) - hash ) + chr;
      // Convert to 32bit integer
      hash |= 0;
    }

    return Number( hash ).toString( 36 );
  }

  /**
   * XOR a string
   *
   * Based on XOR Crypt v1.1.1 - http://github.com/RobLoach/xor-crypt
   * @license MIT
   *   http://opensource.org/licenses/MIT
   *
   * @param {string} str Input
   * @param {number} key Number to apply
   * @returns {string} Output
   */
  function xor( str, key ) {
    return str.split( '' )
      .map( letter => String.fromCharCode( key ^ letter.charCodeAt( 0 ) ) )
      .join( '' );
  }

  let b64Decoded;

  try {
    b64Decoded = window.atob( encoded );
  } catch ( err ) {
    return null;
  }

  const m = b64Decoded.match( /^(\w+)\.(\w+)\.(.*)/ );
  if ( !m ) {
    // Looks wrong
    return null;
  }

  const [ , keyB36, hashExpected, xored ] = m;
  const key = parseInt( keyB36, 36 );
  const plain = xor( xored, key );

  return hashCode( plain ) === hashExpected ? plain : null;
}

export {
  encodeNameInUrl,
  decodeNameFromUrl
};
