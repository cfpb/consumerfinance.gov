'use strict';

var isArray = require( './util/type-checkers' ).isArray;

var Analytics = {

  tagManagerIsLoaded: false,

  EVENT_CATEGORY: 'CFGOV Event',

  /**
   * Initialize the Analytics module.
   */
  init: function() {
    // detect if Google tag manager is loaded
    if ( window.hasOwnProperty( 'google_tag_manager' ) ) {
      Analytics.tagManagerIsLoaded = true;
    } else {
      var _tagManager;
      Object.defineProperty( window, 'google_tag_manager', {
        enumerable: true,
        configurable: true,
        get: function() {
          return _tagManager;
        },
        set: function( value ) {
          _tagManager = value;
          Analytics.tagManagerIsLoaded = true;
        }
      } );
    }
  },

  /**
   * @name sendEvent
   * @kind function
   *
   * @description
   * Pushes an event to the GTM dataLayer.
   *
   * @param {string} action Name of event.
   * @param {string} label DOM element label.
   * @param {Function} callback Function to call on GTM submsission.
   * @param {number} timeout Callback invocation fallback time.
  * @returns {Analytics} An instance
   */
  sendEvent: function( action, label, callback, timeout ) {
    var dataLayerOptions = {
      event:        Analytics.EVENT_CATEGORY,
      action:       action,
      label:        label || '',
      eventTimeout: timeout || 500
    };


    if ( Analytics.tagManagerIsLoaded ) {
      if ( callback ) {
        dataLayerOptions.eventCallback = callback;
      }
      window.dataLayer.push( dataLayerOptions );
    } else if ( typeof callback === 'function' ) {
      return callback();
    }

    return Analytics;
  },

  /**
   * @name sendEvents
   * @kind function
   *
   * @description
   * Pushes multiple events to the GTM dataLayer.
   *
   * @param {array} eventsArray Array of event objects.
   */
  sendEvents: function( eventsArray ) {
    if ( isArray( eventsArray ) ) {
      for ( var i = 0, len = eventsArray.length; i < len; i++ ) {
        Analytics.sendEvent( eventsArray[i] );
      }
    }
  }

};

Analytics.init();

module.exports = Analytics;
