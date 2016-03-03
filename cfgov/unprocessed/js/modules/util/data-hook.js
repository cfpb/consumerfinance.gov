'use strict';

// Required modules.
var standardType = require( './standard-type' );

/**
 * @param {HTMLNode} element - DOM element.
 * @param {string} attr
 *   Attribute to add to the JS data-* hook value.
 * @throws {Error} If supplied value contains a space,
 *   which would mean it would be two values, which is likely a typo.
 * @returns {string} The value that was added.
 */
function add( element, attr ) {
  if ( attr.indexOf( ' ' ) !== -1 ) {
    var msg = standardType.JS_HOOK + 'values cannot contain spaces!';
    throw new Error( msg );
  }
  var values = element.getAttribute( standardType.JS_HOOK );
  element.setAttribute( standardType.JS_HOOK, values + ' ' + attr );

  return attr;
}

/**
 * @param {HTMLNode} element - DOM element.
 * @param {string} attr
 *   Attribute to remove from the JS data-* hook value.
 * @returns {boolean} True if value was removed, false otherwise.
 */
function remove( element, attr ) {
  var values = element.getAttribute( standardType.JS_HOOK );
  var index = values.indexOf( attr );
  var attrs = values.split( ' ' );
  if ( index > -1 ) {
    attrs.splice( index, 1 );
    element.setAttribute( standardType.JS_HOOK, attrs.join( ' ' ) );
    return true;
  }
  return false;
}

/**
 * @param {HTMLNode} element - DOM element.
 * @param {string} attr
 *   Attribute to check as existing as a JS data-* hook value.
 * @returns {boolean} True if the data-* hook value exists, false otherwise.
 */
function contains( element, attr ) {
  var values = element.getAttribute( standardType.JS_HOOK );
  // TODO: This will match variations on the class name,
  //       like 'flyout-menu-var', which would not be correct.
  //       IndexOf should be updated to use a regex instead.
  return values.indexOf( attr ) > -1 ? true : false;
}

module.exports = {
  add:      add,
  contains: contains,
  remove:   remove
};
