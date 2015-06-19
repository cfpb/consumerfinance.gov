/* ==========================================================================
   External Site Initialization
   Used on at least `/external-site/`.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
var handlebars = require( 'handlebars' );

// Instantiate ExternalSite class
// if external-site_container present on page.
function init() {
  var $externalSiteContainer = $( '.external-site_container' );
  if ( $externalSiteContainer.length ) {
    new ExternalSite( $externalSiteContainer );
  }
}

/**
* ExternalSite constructor.
* @class
* @param {HTMLElement} $element DOM Element.
*/
function ExternalSite( $element ) {
  this.$element = $element;
  this.init();
}

// ExternalSite methods and shared properties.
ExternalSite.prototype = {

  duration: 5,

  interval: 1000,

  template: handlebars
            .compile( '<span class=\'external-site_reload-duration\'>' +
                        '{{ duration }}</span>' +
                      ' second{{ plurality }}'
                    ),

  init: function() {
    var self = this;
    self.$durationEl = self.$element
                       .find( '.external-site_reload-container' );

    self.updateContent( self.duration-- );

    self.intervalId = window.setInterval( function() {
      self.updateContent( self.duration-- );
    }, self.interval );

    self.initEvents();
  },

  initEvents: function() {
    this.$element
    .on( 'click', '.external-site_proceed-btn', function( e ) {
      e.stopImmediatePropagation();
    } );
  },

  updateContent: function( duration ) {
    if ( duration === 0 ) {
      clearInterval( this.intervalId );
      window.location = this.$durationEl.data( 'url' );
    } else {
      this.$durationEl.html( this.template( {
        duration:  duration,
        plurality: duration !== 1 ? 's' : ''
      } ) );
    }
  }
};

// Expose public methods.
module.exports = { init: init };
