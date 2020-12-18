import EventObserver from '@cfpb/cfpb-atomic-component/src/mixins/EventObserver.js';
import typeCheckers from '@cfpb/cfpb-atomic-component/src/utilities/type-checkers';

const eventObserver = new EventObserver();
const Analytics = {

  tagManagerIsLoaded: false,
  addEventListener: eventObserver.addEventListener,
  removeEventListener: eventObserver.removeEventListener,
  dispatchEvent: eventObserver.dispatchEvent,

  EVENT_CATEGORY: 'Page Interaction',

  /**
   * Get data layer object.
   * @param {string} action Name of event.
   * @param {string} label DOM element label.
   * @param {string} category Type of event.
   * @param {Function} callback Function to call on GTM submission.
   * @param {number} timeout Callback invocation fallback time.
   * @returns {object} Data layer object.
   */
  getDataLayerOptions: function( action, label, category, callback, timeout ) {
    return {
      event:         category || Analytics.EVENT_CATEGORY,
      action:        action,
      label:         label || '',
      eventCallback: callback,
      eventTimeout:  timeout || 500
    };
  },

  /**
   * Initialize the Analytics module.
   */
  init: function() {
    // detect if Google tag manager is loaded
    if ( window.hasOwnProperty( 'google_tag_manager' ) ) {
      Analytics.tagManagerIsLoaded = true;
    } else {
      let _tagManager;
      Object.defineProperty( window, 'google_tag_manager', {
        enumerable: true,
        configurable: true,
        get: function() {
          return _tagManager;
        },
        set: function( value ) {
          _tagManager = value;
          if ( !Analytics.tagManagerIsLoaded ) {
            Analytics.tagManagerIsLoaded = true;
            Analytics.dispatchEvent( 'gtmLoaded' );
          }
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
   * @param {object} dataLayerOptions Type of event.
   */
  sendEvent: function( dataLayerOptions ) {
    const callback = dataLayerOptions.eventCallback;
    if ( Analytics.tagManagerIsLoaded ) {
      window.dataLayer.push( dataLayerOptions );
    } else if ( callback && typeof callback === 'function' ) {
      // eslint-disable-next-line callback-return
      callback();
    }
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
    if ( typeCheckers.isArray( eventsArray ) ) {
      for ( let i = 0, len = eventsArray.length; i < len; i++ ) {
        Analytics.sendEvent( eventsArray[i] );
      }
    }
  }

};

Analytics.init();

export default Analytics;
