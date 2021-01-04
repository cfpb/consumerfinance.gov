// Required modules.
import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import Analytics from '../modules/Analytics';

const BASE_CLASS = 'o-audio-player';
const EVENT_CATEGORY = 'Audio Player Events';


/**
 * AudioPlayer
 * @class
 *
 * @classdesc Initializes a new AudioPlayer organism for the purpose of sending
 * analytics events for the native HTML `audio` element.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {AudioPlayer} An instance.
 */
function AudioPlayer( element ) { // eslint-disable-line max-lines-per-function
  const _dom = checkDom( element, BASE_CLASS );

  /**
   * @returns {AudioPlayer} An instance.
   */
  function init() {
    if ( !setInitFlag( _dom ) ) {
      return this;
    }

    const label = _dom.dataset.title;

    // Set percentage complete tracker to our first milestone of 25%
    let pctComplete = 25;

    _dom.addEventListener(
      'play',
      function sendEvent() {
        Analytics.sendEvent( {
          event: EVENT_CATEGORY,
          action: 'Play',
          label: label
        } );
      }
    );
    _dom.addEventListener(
      'pause',
      function sendEvent() {
        const currentTime = Math.round( event.target.currentTime );
        const pct = Math.ceil( 100 * currentTime / event.target.duration );

        if ( pct !== 100 ) {
          Analytics.sendEvent( {
            event: EVENT_CATEGORY,
            action: `Paused at ${ pct }%`,
            label: label
          } );
        }
      }
    );
    _dom.addEventListener(
      'ended',
      function sendEvent() {
        Analytics.sendEvent( {
          event: EVENT_CATEGORY,
          action: 'Listened to end',
          label: label
        } );
      }
    );
    _dom.addEventListener(
      'timeupdate',
      function sendEvent() {
        const currentTime = Math.round( event.target.currentTime );
        const pct = Math.floor( 100 * currentTime / event.target.duration );

        /* We just want to send the percent events once, so compare current time
           with the current value of the percentage complete tracker and send
           the event if this is the first pct that is greater than or equal to
           the current milestone. */
        if ( pct >= pctComplete && pct <= 75 ) {
          Analytics.sendEvent( {
            event: EVENT_CATEGORY,
            action: `Reached ${ pctComplete }%`,
            label: label
          } );

          /* Increase percentage complete tracker by 25% so it doesn't send
             an event again until the next milestone is reached. */
          pctComplete += 25;
        }
      }
    );

    return this;
  }

  this.init = init;

  return this;
}

AudioPlayer.BASE_CLASS = BASE_CLASS;

export default AudioPlayer;
