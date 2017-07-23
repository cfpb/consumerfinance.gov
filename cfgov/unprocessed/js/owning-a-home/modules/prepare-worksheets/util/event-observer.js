'use strict';

// TODO: Use EventObserver.js in cfgov-refresh instead.
//       https://github.com/cfpb/cfgov-refresh/
//       blob/flapjack/cfgov/unprocessed/js/modules/util/EventObserver.js

// Used for creating an object that can be used to dispatch and listen
// to custom events.

/**
 * @param {Object} target - An object to attach event listener methods to.
 * @returns {Object} The object that event listener methods are attach to.
 */
function attach( target ) {
  var proxy = new EventObserver();
  target.addEventListener = proxy.addEventListener;
  target.removeEventListener = proxy.removeEventListener;
  target.dispatchEvent = proxy.dispatchEvent;
  return target;
}

function EventObserver() {

  // The events registered on this instance.
  var _events = {};

  /**
   * Register an event listener.
   * @param {string} evt - The event name to listen for.
   * @param {Function} callback - The function called when the event has fired.
   * @returns {EventObserver} An instance.
   */
  function addEventListener( evt, callback ) {
    if ( _events.hasOwnProperty( evt ) ) {
      _events[evt].push( callback );
    } else {
      _events[evt] = [ callback ];
    }

    return this;
  }

  /**
   * Remove an added event listener.
   * Must match a call made to addEventListener.
   * @param {string} evt - The event name to remove.
   * @param {Function} callback - The function attached to the event.
   * @returns {EventObserver} An instance.
   */
  function removeEventListener( evt, callback ) {
    if ( !_events.hasOwnProperty( evt ) ) {
      return this;
    }

    var index = _events[evt].indexOf( callback );
    if ( index !== -1 ) {
      _events[evt].splice( index, 1 );
    }

    return this;
  }

  /**
   * Broadcast an event.
   * @param {string} evt - The type of event to broadcast.
   * @param {Object} options - The event object to pass to the event handler.
   * @returns {EventObserver} An instance.
   */
  function dispatchEvent( evt, options ) {
    if ( !_events.hasOwnProperty( evt ) ) {
      return this;
    }

    options = options || {};

    var evts = _events[evt];
    for ( var i = 0, len = evts.length; i < len; i++ ) {
      evts[i].call( this, options );
    }

    return this;
  }

  return {
    addEventListener:    addEventListener,
    removeEventListener: removeEventListener,
    dispatchEvent:       dispatchEvent
  };
}

// Expose public methods.
this.attach = attach;
