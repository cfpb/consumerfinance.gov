/* ==========================================================================
   PostFilter Initialization
   Used on pages that have post filters.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
var dateRangeFormatter = require( './util/date-range-formatter' );

function init() {
  /**
  * Create the jQuery PostFilter plugin.
  * @param {Object} options Object used to customize PostFilter.
  * @returns {Object} jQuery element.
  */
  $.fn.createPostFilter = function( options ) {
    options = $.extend( true, {}, options );

    return this.each( function() {
      $( this ).data( 'plugin', new PostFilter( this, options ) );
    } );
  };

  return $( '.js-post-filter' ).createPostFilter();
}

/**
* PostFilter constructor.
* @class
* @param {HTMLElement} element DOM Element.
* @param {Object} options Object used to customize PostFilter.
*/
function PostFilter( element, options ) {
  this.$element = $( element );
  $.extend( true, this, this.defaults, options );
  this.init();
}

// PostFilter methods and shared properties
PostFilter.prototype = {

  constructor: PostFilter,

  defaults: {
    dateFormat: 'mm/dd/yyyy'
  },

  init: function() {
    this.bindAll();
    this.initUI();

    return this;
  },

  destroy: function() {
    var self = this;
    this.$element.remove();

    $.each( this, function( key ) {
      delete self[key];
    }, this );

    return this;
  },

  bindAll: function() {
    var self = this;
    var proxy = $.proxy;

    // TODO: Swap this out for Function.bind
    // and Object.keys.
    $.each( this, function( key, _function ) {
      if ( $.isFunction( _function ) ) {
        self[key] = proxy( _function, self );
      }
    } );

    return this;
  },

  initUI: function() {
    var $ui = this.$element;
    var $gte = this.$gte = $ui.find( '.js-filter_range-date__gte' );
    var $lte = this.$lte = $ui.find( '.js-filter_range-date__lte' );

    // Update elements to use the proper placeholder text.
    var dateFormat = this.defaults.dateFormat;
    $gte.attr( 'placeholder', dateFormat );
    $lte.attr( 'placeholder', dateFormat );
    $ui.find( '.ie-date_format' ).html( '(' + dateFormat + ')' );

    // Add listener for submit event.
    $ui.on( 'submit', 'form', this.onSubmit );

    return this;
  },

  onSubmit: function( e ) {
    var dateRange = dateRangeFormatter.format( this.$gte.val(), this.$lte.val() );
    if ( dateRange && dateRange.isValid ) {
      this.$gte.val( dateRange.startDate );
      this.$lte.val( dateRange.endDate );
    } else {
      e.preventDefault();
      // TODO: Add inline notifcation;
    }

    return this;
  }
};

// Expose public methods.
module.exports = { init: init };
