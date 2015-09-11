/* ==========================================================================
 Polyfill for Array forEach.
 Copied from https://developer.mozilla.org/en-US/docs/Web
 /JavaScript/Reference/Global_Objects/Array/forEach.

 Production steps of ECMA-262, Edition 5, 15.4.4.18.
 Reference: http://es5.github.io/#x15.4.4.18
 ========================================================================== */

'use strict';

if ( !Array.prototype.forEach ) {
  // Ignore complexity eslint offense for polyfill.
  Array.prototype.forEach = function( callback, thisArg ) { //eslint-disable-line

    var T, k;

    if ( this === null ) {
      throw new TypeError( ' this is null or not defined' );
    }

    // 1. Let O be the result of calling
    //    ToObject passing the |this| value as the argument.
    var O = Object( this );

    // 2. Let lenValue be the result of calling
    //    the Get internal method of O with the argument "length".

    // 3. Let len be ToUint32(lenValue).
    var len = O.length >>> 0;

    // 4. If IsCallable(callback) is false, throw a TypeError exception.
    //    See: http://es5.github.com/#x9.11
    if ( typeof callback !== 'function' ) {
      throw new TypeError( callback + ' is not a function' );
    }

    // 5. If thisArg was supplied, let T be thisArg; else let T be undefined.
    if ( arguments.length > 1 ) {
      T = thisArg;
    }

    // 6. Let k be 0.
    k = 0;

    // 7. Repeat, while k < len.
    while ( k < len ) {

      var kValue;

      // a. Let Pk be ToString(k).
      //    This is implicit for LHS operands of the in operator.
      // b. Let kPresent be the result of calling
      //    the HasProperty internal method of O with argument Pk.
      //    This step can be combined with c
      // c. If kPresent is true, then
      if ( k in O ) {

        // i. Let kValue be the result of calling
        //    the Get internal method of O with argument Pk.
        kValue = O[k];

        // ii. Call the Call internal method of
        //     callback with T as the this value and
        //     argument list containing kValue, k, and O.
        callback.call( T, kValue, k, O );
      }
      // d. Increase k by 1.
      k++;
    }
    // 8. return undefined
  };
}
