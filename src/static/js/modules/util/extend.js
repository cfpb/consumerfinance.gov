/* ==========================================================================
   Extend

   Code copied from the following with minimal modification :

   - https://github.com/AmpersandJS/
     ampersand-class-extend/blob/master/ampersand-class-extend.js

   - http://backbonejs.org/#
   ========================================================================== */

'use strict';

var _assign = require( './assign' );

// Helper function to correctly set up the prototype chain, for subclasses.
// Similar to `goog.inherits`, but uses a hash of prototype properties and
// class properties to be extended.
var extend = function extend( protoProps ) {
  var parent = this;
  var child;
  var args = [].slice.call( arguments );

  // The constructor function for the new subclass is either defined by you
  // (the "constructor" property in your `extend` definition), or defaulted
  // by us to simply call the parent's constructor.
  if ( protoProps && protoProps.hasOwnProperty( 'constructor' ) ) {
    child = protoProps.constructor;
  } else {
    child = function () {
      return parent.apply( this, arguments );
    };
  }

  // Add static properties to the constructor function from parent
  _assign( child, parent );

  // Set the prototype chain to inherit from `parent`, without calling
  // `parent`'s constructor function.
  var Surrogate = function() { this.constructor = child; };
  Surrogate.prototype = parent.prototype;
  child.prototype = new Surrogate();

  // Mix in all prototype properties to the subclass if supplied.
  if ( protoProps ) {
    args.unshift( child.prototype );
    _assign.apply( null, args );
  }

  // Set a convenience property in case the parent's prototype is needed
  // later.
  child.__super__ = parent.prototype;

  return child;
};

// Expose the extend function
module.exports = extend;
