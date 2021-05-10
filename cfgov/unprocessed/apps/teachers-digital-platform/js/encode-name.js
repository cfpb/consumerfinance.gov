/**
 * Create a hash code for a string
 *
 * Adapted from https://stackoverflow.com/a/7616484/3779
 *
 * @param {string} str String to hash
 * @returns {string} Hash code
 */
function hashCode( str ) {
  if ( str.length === 0 ) {
    return '0';
  }

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

// Some simple obfuscation when minified
const wwindow = window;
const xtoy = 'xtoy';
const a = 'a';
const b = 'b';
const x = 'x';
const y = 'y';
const btoa = xtoy.replace( x, b ).replace( y, a );
const atob = xtoy.replace( x, a ).replace( y, b );

/**
 * Encode string randomly with checksum
 * 
 * -> base64("<base32(xorKey)>.<hash>.<xoredString>")
 *
 * @param {string} input Input
 * @returns {string} Encoded string
 */
function encode( input ) {
  const attempt = key => {
    const keyB36 = Number( key ).toString( 36 );
    const xored = xor( input, key );
    const hash = hashCode( input );

    return wwindow[btoa](
      [keyB36, hash, xored].join( '.' )
    );
  };

  // Sometimes random gets ugly
  const uglies = [ /[a@][s$][s$]/i, /b[i1][t+]ch/i, /(f|ph)u[ck]/i ];
  const key = Math.ceil( Math.random() * 100 );

  // Try keys until no uglies
  for ( let i = 0; i < 100; i++ ) {
    const out = attempt( key + i );
    const isUgly = uglies.some( patt => patt.test( out ) );
    if ( !isUgly ) {
      return out;
    }
  }

  // Oh well
  return attempt( key );
}

/**
 * Decode a string
 *
 * @param {string} encoded Encoded string
 * @returns {string | null} Decoded string (or null)
 */
function decode( encoded ) {
  let b64Decoded;

  try {
    b64Decoded = wwindow[atob]( encoded );
  } catch ( err ) {
    return null;
  }

  const m = b64Decoded.match( /^(\w+)\.(\w+)\.(.*)/ );
  if ( !m ) {
    // Looks wrong
    return null;
  }

  const [, keyB36, hashExpected, xored] = m;
  const key = parseInt( keyB36, 36 );
  const plain = xor( xored, key );

  return hashCode( plain ) === hashExpected ? plain : null;
}

/**
 * Store name in session storage
 *
 * @param {string} name Name
 */
function storeName( name ) {
  sessionStorage.setItem( 'tdp-name', encode( name ) );
}

/**
 * Retrieve validated name from session storage
 *
 * @returns {string | null} Name, if set and valid
 */
function recallName() {
  const str = sessionStorage.getItem( 'tdp-name' );

  return str === null ? null : decode( str );
}

/**
 * Remove encoded name from session storage
 */
function forgetName() {
  sessionStorage.removeItem( 'tdp-name' );
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

export {
  storeName,
  recallName,
  forgetName,
  encodeNameInUrl,
  decodeNameFromUrl
};
