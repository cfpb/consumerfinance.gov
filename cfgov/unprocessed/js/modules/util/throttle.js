'use strict';

/**
 * @name throttle
 * @kind function
 *
 * @description
 * Limits functions calls based on a specified interval.
 *
 * @param {function} func Function to invoke.
 * @param {number} wait Time interval to wait before invoking function.
 * @param {Object} options Confinguration object used to control leading
 *                         and tailing wait times.
 * @returns {*} Result of function invocation.
 */
function throttle( func, wait, options ) {
  var context;
  var args;
  var result;
  var timeout = null;
  var previous = 0;
  if ( !options ) options = {};

  /**
   * Function wrapper used to invoke 'func' argument
   * after wait interval.
   */
  function _later() {
    previous = options.leading === !1 ? 0 : Date.now();
    timeout = null;
    result = func.apply( context, args );
    if ( !timeout ) context = args = null;
  }

  return function() {
    var now = Date.now();
    if ( !previous && options.leading === !1 ) previous = now;
    var remaining = wait - ( now - previous );
    context = this;
    args = arguments;
    if ( remaining <= 0 || remaining > wait ) {
      if ( timeout ) {
        clearTimeout( timeout );
        timeout = null;
      }
      previous = now;
      result = func.apply( context, args );
      if ( !timeout ) context = args = null;
    } else if ( !timeout && options.trailing !== !1 ) {
      timeout = setTimeout( _later, remaining );
    }
    return result;
  };
}

module.exports = { throttle: throttle };
