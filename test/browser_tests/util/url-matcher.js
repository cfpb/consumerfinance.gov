/* ==========================================================================
   URL matcher
   ========================================================================== */


/**
 * Returns absolute URL.
 *
 * @param {string} url - A string containing a URL.
 * @returns {string} - An absolute URL.
 */
function _getAbsoluteUrl( url ) {
  if ( url ) {
    url = url.indexOf( 'http' ) > -1 ? url : browser.baseUrl + url;
  }

  return url;
}

/**
 * Custom Jasmine matcher to compare URLs.
 *
 * @param {object} util - Object containing Jasmine utility functions.
 * @param {object} customEqualityTesters
 *   - Object containing Jasmine equality functions.
 * @returns {object} -  Object containing compare function.
 */
function toEqualUrl( util, customEqualityTesters ) {

  /**
   * Custom Jasmine matcher to compare URLs.
   *
   * @param {string|array} actual - A string or array of URLs.
   * @param {string|array} expected - A string or array of URLs.
   *
   * @returns {object} - Jasmine result object.
   */
  function compare( actual, expected ) {
    let message;
    const result = {};

    if ( Array.isArray( expected ) ) {
      expected = expected.map( function( url ) {
        return _getAbsoluteUrl( url );
      } );
    } else {
      expected = _getAbsoluteUrl( expected );
    }

    result.pass = util.equals( actual, expected, customEqualityTesters );

    message = 'Expected ' + actual + ' to equal ' + expected;

    if ( !result.pass ) {
      message += ', but it does not';
    }

    result.message = message + '.';

    return result;
  }

  return { compare: compare };
}


// Expose public methods.
module.exports = { toEqualUrl: toEqualUrl };
