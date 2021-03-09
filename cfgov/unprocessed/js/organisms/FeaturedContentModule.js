/* ==========================================================================
   Featured Content Module Class
   ========================================================================== */

// Required modules.
import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import VideoPlayer from './VideoPlayer';

const BASE_CLASS = 'o-featured-content-module';

/**
 * FeaturedContentModule
 * @class
 *
 * @classdesc Initializes a new FeaturedContentModule organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {FeaturedContentModule} An instance.
 */
function FeaturedContentModule( element ) {
  const _dom = checkDom( element, BASE_CLASS );

  let _videoPlayer = null;

  /**
   * @returns {FeaturedContentModule|undefined} An instance.
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !setInitFlag( _dom ) ) {
      let UNDEFINED;
      return UNDEFINED;
    }

    const videoPlayerDom = _dom.querySelector( `.${ VideoPlayer.BASE_CLASS }` );

    // If we don't have a video in this FCM, bail out.
    if ( videoPlayerDom === null ) {
      return this;
    }

    _videoPlayer = new VideoPlayer( videoPlayerDom );
    _videoPlayer.addEventListener( 'onPlay', _videoPlayHandler.bind( this ) );
    _videoPlayer.addEventListener( 'onStop', _videoStopHandler.bind( this ) );
    _videoPlayer.init();

    return this;
  }

  /**
   * Event handler for when video has begun playing.
   */
  function _videoPlayHandler() {
    _dom.classList.add( 'video-playing' );
  }

  /**
   * Event handler for when video has stopped playing.
   */
  function _videoStopHandler() {
    _dom.classList.remove( 'video-playing' );
  }

  this.init = init;

  return this;
}

FeaturedContentModule.BASE_CLASS = BASE_CLASS;

export default FeaturedContentModule;
