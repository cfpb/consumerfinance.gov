/* ==========================================================================
   Featured Content Module Class
   ========================================================================== */

// Required modules.
import { checkDom, setInitFlag } from '../modules/util/atomic-helpers';
import VideoPlayer from './VideoPlayer';

const BASE_CLASS = 'o-featured-content-module';

let _dom;
let _videoPlayer;

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
  _dom = checkDom( element, BASE_CLASS );

  this.init = init;

  return this;
}

/**
 * @returns {FeaturedContentModule} An instance.
 */
function init() {
  setInitFlag( _dom );

  _videoPlayer = new VideoPlayer( _dom.querySelector( `.${ VideoPlayer.BASE_CLASS }` ) );
  _videoPlayer.addEventListener( 'onPlay', _videoPlayHandler );
  _videoPlayer.addEventListener( 'onStop', _videoStopHandler );
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

FeaturedContentModule.BASE_CLASS = BASE_CLASS;

export default FeaturedContentModule;
