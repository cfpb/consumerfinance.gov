'use strict';

/**
 * EventObserver
 * @class
 *
 * @classdesc Used for creating an object
 *   that can be used to dispatch and listen to custom events.
 * @returns {Object} An EventObserver instance.
 */
function EventObserver() {

  // The events registered on this instance.
  var _events = {};

  /**
   * Register an event listener.
   * @param {string} evt The event name to listen for.
   * @param {Function} callback The function called when the event has fired.
   * @returns {Object} The instance this EventObserver instance is decorating.
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
   * @param {string} evt The event name to remove.
   * @param {Function} callback The function attached to the event.
   * @returns {Object} The instance this EventObserver instance is decorating.
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
   * @param {string} evt The type of event to broadcast.
   * @param {Object} options The event object to pass to the event handler.
   * @returns {Object} The instance this EventObserver instance is decorating.
   */
  function dispatchEvent( evt, options ) {
    if ( !_events.hasOwnProperty( evt ) ) {
      return this;
    }

    options = options || {};

    var evts = _events[evt];
    for ( var e = 0, len = evts.length; e < len; e++ ) {
      evts[e].call( this, options );
    }

    return this;
  }

  EventObserver.prototype.addEventListener = addEventListener;
  EventObserver.prototype.removeEventListener = removeEventListener;
  EventObserver.prototype.dispatchEvent = dispatchEvent;
  return this;
}

module.exports = EventObserver;
