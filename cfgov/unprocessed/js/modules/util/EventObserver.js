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
   * @param {string} event - The event name to listen for.
   * @param {Function} callback - The function called when the event has fired.
   * @returns {Object} The instance this EventObserver instance is decorating.
   */
  function addEventListener( event, callback ) {
    if ( _events.hasOwnProperty( event ) ) {
      _events[event].push( callback );
    } else {
      _events[event] = [ callback ];
    }

    return this;
  }

  /**
   * Remove an added event listener.
   * Must match a call made to addEventListener.
   * @param {string} event - The event name to remove.
   * @param {Function} callback - The function attached to the event.
   * @returns {Object} The instance this EventObserver instance is decorating.
   */
  function removeEventListener( event, callback ) {
    if ( !_events.hasOwnProperty( event ) ) {
      return this;
    }

    var index = _events[event].indexOf( callback );
    if ( index !== -1 ) {
      _events[event].splice( index, 1 );
    }

    return this;
  }

  /**
   * Broadcast an event.
   * @param {string} event - The type of event to broadcast.
   * @param {Object} options - The event object to pass to the event handler.
   * @returns {Object} The instance this EventObserver instance is decorating.
   */
  function dispatchEvent( event, options ) {
    if ( !_events.hasOwnProperty( event ) ) {
      return this;
    }

    options = options || {};

    var evts = _events[event];
    for ( var i = 0, len = evts.length; i < len; i++ ) {
      evts[i].call( this, options );
    }

    return this;
  }

  EventObserver.prototype.addEventListener = addEventListener;
  EventObserver.prototype.removeEventListener = removeEventListener;
  EventObserver.prototype.dispatchEvent = dispatchEvent;
  return this;
}

module.exports = EventObserver;
