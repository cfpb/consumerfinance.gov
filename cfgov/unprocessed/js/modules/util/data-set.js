'use strict';

/**
 * Converts a string from selector-case to camelCase (e.g. from
 * @param {string} str The string in selector-case form.
 * @return {string} The string in camelCase form.
 */
function _toCamelCase( str ) {
  return str.replace( /\-([a-z])/g, function( all, match ) {
    return match.toUpperCase();
  } );
};

/**
 * Get dataset from dom element.
 * @param {string} str The string in selector-case form.
 * @return {object} The data set.
 * Contains code copied from https://github.com/remy/polyfills/blob/master/dataset.js.
 */
function dataSet( element ) {
  var dataset = {};
  var regex = /^data-(.+)/;
  if ( document.documentElement.dataset ) return element.dataset;

  for( var i = 0; i < element.attributes.length; i++ ) {
    var attr = element.attributes[i];
    if ( match = attr.name.match( regex ) ) {
      dataset[_toCamelCase( match[1] )] = attr.value;
    }
  }

  return dataset;
}

// Expose public methods.
module.exports = { dataSet: dataSet };
