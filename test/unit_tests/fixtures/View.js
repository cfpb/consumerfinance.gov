'use strict';

/* ==========================================================================
   View

   Backbone inspired minimal MVC view.

   Code convetions copied from the following with minimal modifications:

   - http://backbonejs.org/docs/backbone.html.

   - http://ampersandjs.com/learn/view-conventions.

   ========================================================================== */

// All views accept an options object
// as the first argument to their constructor.
function View( options ) {
  if ( options && options.el ) this.el = options.el;
  this.initialize.apply( this, arguments );
}

View.prototype = {

  rendered: false,

  // After View is instatiated, initialize should have been called.
  initialize: function() {},

  // After render is called the following should be true :
  // - instances should have rendered set to true.
  // - this.el should be bound to a dom element.
  render: function() {
    this.rendered = true;
    if ( !this.el ) {
      this.el = document.createElement( 'div' );
    }

    return this;
  },

  // After remove is called the following should be true :
  // - this.el removed from dom.
  // - this.el reference should be undefined.
  remove: function() {
    if ( this.el ) {
      var parent = this.el.parentNode;
      if ( parent ) parent.removeChild( this.el );
      delete this.el;
    }

    return this;
  }

};

module.exports = View;
