/* ==========================================================================
   Events

   Lightweight mixin to add basic event callback functionality.
   ========================================================================== */

'use strict';

var Events = {

  on: function( eventName, callback ) {
    this.events[eventName] = this.events[eventName] || [];
    this.events[eventName].push( callback );

    return this;
  },

  off: function( eventName ) {
    if ( this.events[eventName] ) delete this.events[eventName];
  },

  trigger: function( eventName ) {
    this.events[eventName] = this.events[eventName] || [];
    for ( var i = 0, len = this.events[eventName].length; i < len; i++ ) {
      this.events[eventName][i].apply( this, arguments );
    }

    return this;
  }

};

module.exports = Events;
