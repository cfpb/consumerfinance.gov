/* ==========================================================================
 Polyfill for Function bind.

 Code copied from the following with minimal modification :

 - https://developer.mozilla.org/en-US/docs/Web/
   JavaScript/Reference/Global_Objects/Function/bind.
 ========================================================================== */

'use strict';

if ( !Function.prototype.bind ) {
  Function.prototype.bind = function( oThis ) {
    if ( typeof this !== 'function' ) {
      // closest thing possible to the ECMAScript 5
      // internal IsCallable function
      throw new TypeError(
        'Function.prototype.bind - what is trying to be bound is not callable'
      );
    }

    var aArgs = Array.prototype.slice.call( arguments, 1 );
    var fToBind = this;
    function FNOP() {}
    function fBound() {
      return fToBind.apply( this instanceof FNOP
             ? this
             : oThis,
             aArgs.concat( Array.prototype.slice.call( arguments ) ) );
    }

    FNOP.prototype = this.prototype;
    fBound.prototype = new FNOP();

    return fBound;
  };
}
