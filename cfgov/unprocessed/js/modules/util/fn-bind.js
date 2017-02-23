/* ==========================================================================
   fnBind

   Code copied from the following with minimal modifications :

   - https://raw.githubusercontent.com/Modernizr/Modernizr/
     74655c45ad2cd05c002e4802cdd74cba70310f08/src/fnBind.js

   Polyfill for BlackBerry 7. IE8- gets a simplified no-js page.
   To test whether the polyfill is needed by a particular browser,
   the following code can temporarily be placed in the document <head>:

   alert( typeof Function.prototype.bind == 'function' );
   ========================================================================== */

'use strict';


/**
* Function.prototype.bind polyfill.
*
* @access private
* @function fnBind
* @param {Function} fn - A function you want to change `this` reference to.
* @param {Object} context - The `this` you want to call the function with.
* @returns {Function} The wrapped version of the supplied function.
*/
function fnBind( fn, context ) {
  return function() {
    return fn.apply( context, arguments );
  };
}


// Expose public methods.
module.exports = { fnBind: fnBind };
