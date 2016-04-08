'use strict';


/**
* Function.Bind polyfill.
*
* @access private
* @function fnBind
* @param {function} fn - a function you want to change `this` reference to
* @param {object} context - the `this` you want to call the function with
* @returns {function} The wrapped version of the supplied function
*/

function fnBind(fn, context) {
  return function() {
    return fn.apply(context, arguments);
  };
}


// Expose public methods.
module.exports = { fnBind: fnBind };
