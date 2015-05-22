/* ==========================================================================
   jquery.cf_notifier
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
var handlebars = require( 'handlebars' );

var _notifierTemplate = '<div class="cf-notification cf-notification__{{ state }}" style="display: none;">' +
  '<span class="cf-notification_icon cf-notification_icon__{{ state }} cf-icon cf-icon-{{ icon }}-round"></span>' +
  '<p class="cf-notification_text">{{ message }}</p>' +
  '</div>';

var _notifier = {
  defaults: {
    message:    'There was an error with your submission',
    state:      'error',
    speed:      400,
    easing:     'swing',
    template:   _notifierTemplate,
    input:      null,
    onRender:   null,
    onClearAll: null,
    onDestroy:  null
  },

  /**
  * Generate a string of HTML from the plugin's settings.
  * @returns {string} The expanded HTML string.
  */
  _generateHTML: function() {
    var data = {
      message: _notifier.settings.message,
      state:   _notifier.settings.state
    };

    if ( data.state === 'success' ) {
      data.icon = 'approved';
    } else if ( data.state === 'warning' ) {
      data.icon = 'error';
    } else {
      data.icon = 'delete';
    }

    var template = handlebars.compile( _notifier.settings.template );

    return template( data );
  },

  // Clear any previously created notifications
  _clearExisting: function( callback ) {
    $( _notifier.existing ).slideUp( {
        speed:    _notifier.settings.speed,
        easing:   _notifier.settings.easing,
        complete: function() {
          $( this ).remove();
          _notifier.existing = false;
          if ( callback ) {
            callback();
          }
        }
    } );
  },

  // Create a notification
  _notify: function( elem ) {
    $( _notifier.html )
      .prependTo( elem )
      .slideDown( _notifier.settings.speed, function() {
        _notifier.existing = this;
        if ( _notifier.settings.onRender ) {
          _notifier.settings.onRender.call( this );
        }
      } );
  },

  // Listen for custom cf_notifier:notify event
  _initNotifyListener: function() {
    _notifier.elem.on( 'cf_notifier:notify', function( event, options ) {
      var elem = $( this );
      _notifier.settings = $.extend( {}, _notifier.settings, options );
      _notifier.html = _notifier._generateHTML( _notifier.settings );
      if ( _notifier.existing ) {
        _notifier._clearExisting( function() {
          _notifier._notify( elem );
        } );
      } else {
        _notifier._notify( elem );
      }
    } );
  },

  // Listen for custom cf_notifier:clear event
  _initClearListener: function() {
    _notifier.elem.on( 'cf_notifier:clear', function( event, options ) {
      _notifier.settings = $.extend( {}, _notifier.settings, options );
      if ( _notifier.existing ) {
        _notifier._clearExisting( function() {
          if ( _notifier.settings.onClearAll ) {
            _notifier.settings.onClearAll.call( this );
          }
        } );
      } else if ( _notifier.settings.onClearAll ) {
        _notifier.settings.onClearAll.call( this );
      }
    } );
  },

  // Remove all custom cf_notifier event listeners
  _rmCFNotifierListeners: function() {
    _notifier.elem.off( 'cf_notifier' );
  },

  init: function( options ) {
    return this.each( function() {
      _notifier.elem = $( this );
      _notifier.settings = $.extend( {}, _notifier.defaults, options );

      if ( _notifier.elem.length > 0 ) {
        _notifier._initNotifyListener();
        _notifier._initClearListener();
      }
    } );
  },

  destroy: function() {
    return this.each( function() {

      _notifier._rmCFNotifierListeners();

      if ( _notifier.existing ) {
        _notifier._clearExisting( function() {
          if ( _notifier.settings.onDestroy ) {
            _notifier.settings.onDestroy.call( this );
          }
          _notifier.settings = [];
        } );
      } else {
        if ( _notifier.settings.onDestroy ) {
          _notifier.settings.onDestroy.call( this );
        }
        _notifier.settings = [];
      }
    } );
  }
};

function init() {
  $.fn.cf_notifier = function() {
    var options;
    var method = arguments[0];

    if ( _notifier[method] ) {
      method = _notifier[method];
      options = Array.prototype.slice.call( arguments, 1 );
    } else if ( typeof method === 'object' || !method ) {
      method = _notifier.init;
      options = arguments;
    } else {
      $.error( 'Method "' + method + '"" does not exist in the cf__notifier plugin' );
      return this;
    }

    return method.apply( this, options );
  };
}

module.exports = { init: init };
