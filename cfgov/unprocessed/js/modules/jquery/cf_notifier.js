/* ==========================================================================
   jquery.cf_notifier
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
var handlebars = require( 'handlebars' );

var _notifierTemplate = '<div class="m-notification ' +
                                    'm-notification__{{ state }}" ' +
                             'style="display: none;">' +
                          '<span class="m-notification_icon cf-icon"></span>' +
                          '<div class="m-notification_content">' +
                              '<p class="h4 m-notification_message">{{{ message }}}</p>' +
                          '</div>' +
                        '</div>';

var _notifier = {
  defaults: {
    message:        'There was an error with your submission',
    state:          'error',
    duration:       200,
    easing:         'swing',
    template:       _notifierTemplate,
    insertLocation: 'prependTo',
    insertTarget:   null,
    input:          null,
    onRender:       null,
    onClearAll:     null,
    onDestroy:      null
  },

  existing: false,

  /**
   * Generate a string of HTML from the plugin's settings
   * @returns {string} The expanded HTML string
  */
  _generateHTML: function() {
    var settings = _notifier.settings;
    var icon = {
      error:   'delete',
      success: 'approved',
      warning: 'error'
    };
    var data = {
      message: settings.message,
      state:   settings.state,
      icon:    icon[settings.state]
    };
    var template = handlebars.compile( settings.template );

    return template( data );
  },

  // Clear any previously created notifications
  _clearExisting: function( callback ) {
    var settings = _notifier.settings;
    $( _notifier.existing ).slideUp( {
      duration: settings.duration,
      easing:   settings.easing,
      complete: function() {
        $( this ).remove();
        _notifier.existing = false;
        if ( callback ) {
          return callback();
        }
      }
    } );
  },

  // Create a notification
  _notify: function( elem ) {
    var settings = _notifier.settings;
    var html = _notifier._generateHTML();
    $( html )[settings.insertLocation]( elem )
      .slideDown( {
        duration: settings.duration,
        easing:   settings.easing,
        complete: function() {
          _notifier.existing = this;
          if ( settings.onRender ) {
            settings.onRender.call( this );
          }
        }
      } );
  },

  // Listen for custom cf_notifier:notify event
  _initNotifyListener: function() {
    _notifier.elem.on( 'cf_notifier:notify', function( event, options ) {
      _notifier.settings = $.extend( {}, _notifier.settings, options );
      var $target = _notifier.settings.insertTarget || $( this );
      if ( _notifier.existing ) {
        _notifier._clearExisting( function() {
          _notifier._notify( $target );
        } );
      } else {
        _notifier._notify( $target );
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
      $.error(
        'Method "' + method + '"" does not exist in the cf__notifier plugin'
      );
      return this;
    }

    return method.apply( this, options );
  };
}

module.exports = { init: init };
