/**
 * Converts (should|shouldn't) to Boolean.
 * @param {string} value - The string value to convert.
 * @returns {boolean} True if 'should', otherwise false.
 */
function shouldShouldnt( value ) {

  return value === 'should' ? true : false;
}

function toCamelCase( value ) {

  return value.replace( /\s(\w)/g, function( matches, letter ) {

    return letter.toUpperCase();
  } );
}

module.exports = {
  shouldShouldnt: shouldShouldnt,
  toCamelCase:    toCamelCase
};
