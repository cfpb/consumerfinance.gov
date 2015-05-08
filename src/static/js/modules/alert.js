/* ==========================================================================
   Alert Initialization
   Used on at least `/the-bureau/leadership-calendar/`.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );

function init() {
  // Create the jQuery Alert plugin.
  // @options {Object} Object used to customize Alert.
  // Returns jQuery element.
  $.fn.createAlert = function( options ) {
    return this.each( function() {
      var $this = $( this );
      $this.data( 'plugin', new Alert( this, options ) );
    } );
  };

  $( '.alert' ).createAlert();
}

// Alert constructor.
// @param element {Element} DOM Element.
// @param options {Object} Object used to customize Alert.
// Returns {Object} An Alert instance.
function Alert( element, options ) {
  this.$element = $( element );
  this.options = $.extend( true, {}, this.defaults, options );
  this.init();
}

// Alert methods and shared properties
Alert.prototype = {

  constructor: Alert,

  defaults: {
    validateSelector: '.js-validate_form-not-empty',
    easing:           'linear'
  },

  init: function() {
    var parentForm = this.$element.parents( this.defaults.validateSelector );

    if ( parentForm.length === 1 ) {
      parentForm.on( 'form:validate:empty', $.proxy( this.show, this ) );
      parentForm.on( 'form:validate:not_empty', $.proxy( this.hide, this ) );
    }
    return this;
  },

  destroy: function() {
    this.$element.removeData();
    return this;
  },

  show: function() {
    this.$element.slideDown( {
      easing: this.defaults.easing
    } );
    return this;
  },

  hide: function() {
    this.$element.slideUp( {
        easing: this.defaults.easing
    } );
    return this;
  }
};


// Expose public methods.
module.exports = { init: init };
