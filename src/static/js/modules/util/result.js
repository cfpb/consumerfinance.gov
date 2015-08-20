/* ==========================================================================
   Result

   Code copied from the following with minimal modification :

   - http://underscorejs.org/docs/underscore.html#section-163.
   ========================================================================== */

'use strict';

var _isFunction = require( '../util/type-checkers' ).isFunction;

function result( object, property, fallback ) {
  var value;

  if ( object !== null ) value = object[property];

  if ( !value ) {
    value = fallback;
  }

  return _isFunction( value ) ? value.call( object ) : value;
}

module.exports = result;
