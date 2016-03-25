'use strict';

/**
 * Converts a string from selector-case to camelCase.
 * @param {string} str - The string in selector-case form.
 * @returns {string} The string in camelCase form.
 */
function _toCamelCase( str ) {
  return str.replace( /\-([a-z])/g, function( all, match ) {
    return match.toUpperCase();
  } );
}

/**
 * Get dataset from DOM element.
 * Contains code copied from
 * https://github.com/remy/polyfills/blob/master/dataset.js.
 * @param {HTMLElement} element - The element to check for dataset support.
 * @returns {Object} The data set.
 */
function dataSet( element ) {
  if ( document.documentElement.dataset ) return element.dataset;

  var dataset = {};
  var regex = /^data-(.+)/;
  var attr;
  var match;
  for ( var i = 0; i < element.attributes.length; i++ ) {
    attr = element.attributes[i];
    match = attr.name.match( regex );
    if ( match ) {
      dataset[_toCamelCase( match[1] )] = attr.value;
    }
  }

  return dataset;
}

// Expose public methods.
module.exports = { dataSet: dataSet };
