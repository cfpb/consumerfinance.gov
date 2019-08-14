/* ==========================================================================
   Video Player Class
   ========================================================================== */

// Required modules.
import { checkDom, setInitFlag } from '../modules/util/atomic-helpers';
import EventObserver from '../modules/util/EventObserver';
import youTubeAPI from '../modules/youtube-api';

const BASE_CLASS = 'o-video-player';

let _dom;
let _imageDom;
let _defaultImageURL;
let _videoId;
let _playLinkDom;
let _playBtnDom;
let _closeBtnDom;
let _iframeDom;
let _player;

let _playVideoBinded;
let _stopVideoBinded;

/**
 * VideoPlayer
 * @class
 *
 * @classdesc Initializes a new VideoPlayer organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {VideoPlayer} An instance.
 */
function VideoPlayer( element ) {

  // Attach event methods.
  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;
  this.removeEventListener = eventObserver.removeEventListener;

  _dom = checkDom( element, BASE_CLASS );
  _videoId = _dom.getAttribute( 'data-id' );
  _imageDom = _dom.querySelector( `.${ BASE_CLASS }_image` );
  _defaultImageURL = _imageDom.src;
  _playLinkDom = _dom.querySelector( `a.${ BASE_CLASS }_play-btn` );
  _playBtnDom = _dom.querySelector( `button.${ BASE_CLASS }_play-btn` );
  _closeBtnDom = _dom.querySelector( `.${ BASE_CLASS }_close-btn` );
  _iframeDom = _dom.querySelector( `.${ BASE_CLASS }_iframe` );

  _playVideoBinded = playVideo.bind( this );
  _stopVideoBinded = stopVideo.bind( this );

  // Expose the public methods.
  this.init = init;

  return this;
}

/**
 * @returns {VideoPlayer} An instance.
 */
function init() {
  setInitFlag( _dom );

  // Retrieve the image URL and load the image.
  let imageURL = '';
  if ( _videoId !== null ) {
    imageURL = youTubeAPI.fetchImageURL( _videoId );
  }
  _imageLoad( imageURL );

  youTubeAPI.attachAPIReadyCallback( _videoAPIReady );
  youTubeAPI.embedVideoScript();

  return this;
}

/**
 * Handler for when the video API has loaded and is ready, in this case when the
 * YouTube IFrame API is done loading.
 */
function _videoAPIReady() {
  _player = youTubeAPI.instantiatePlayer( _iframeDom, _videoId );
  _player.addEventListener( 'onReady', _videoPlayerReadyHandler );
  _player.addEventListener( 'onStateChange', _videoStateChangeHandler );
}

/**
 * Event handler for the when the video is ready.
 */
function _videoPlayerReadyHandler() {

  /* On page load we show a play link that links directly to the video, so that
     the user can still access the video with no JavaScript.
     We need to hide the link and show the play button for the embedded video. */
  _playLinkDom.classList.add( 'u-hidden' );
  _playBtnDom.classList.remove( 'u-hidden' );

  // Add events.
  _playBtnDom.addEventListener( 'click', _playBtnClickedHandler );
  _closeBtnDom.addEventListener( 'click', _closeBtnClickedHandler );

  // The video has loaded.
  _dom.classList.add( `${ BASE_CLASS }__loaded` );
}

/**
 * Handler for when the video changes state.
 * @param {Event} event - Event object for the changed state,
 *   which contains a data property for the state.
 */
function _videoStateChangeHandler( event ) {
  if ( event.data === window.YT.PlayerState.ENDED ) {
    _stopVideoBinded();
  }
}

/**
 * HANDLE THUMBNAIL IMAGE.
 */

/**
 * Load Youtube max res image if it exists.
 * TODO: Replace this method by calling the YouTube data API.
 * https://developers.google.com/youtube/v3/getting-started#fields
 *
 * @param {string} imageURL - The URL to load in the image.
 */
function _imageLoad( imageURL ) {
  _imageDom.addEventListener( 'load', _imageLoadedHandler );
  _imageDom.addEventListener( 'error', () => { _imageLoadDefault(); } );

  _imageDom.src = imageURL;
}

/**
 * Event handler for loading state change (onload)
 * of an image element when the src attribute is set.
 */
function _imageLoadedHandler() {
  /* 120px is the natural width of the default YouTube image.
     This condition will be true when there isn't a custom image set. */
  if ( _imageDom.naturalWidth === 120 ) {
    _imageLoadDefault();
  }
  _imageShow();
}

/**
 * Load the default image source (src) first set at load-time.
 */
function _imageLoadDefault() {
  _imageDom.src = _defaultImageURL;
  _imageShow();
}

/**
 * Show the image by adding a class that changes its opacity.
 */
function _imageShow() {
  _imageDom.classList.add( `${ BASE_CLASS }_image-loaded` );
}

/**
 * HANDLE VIDEO INTERACTIONS.
 */

/**
 * Handler for clicking of the play button.
 */
function _playBtnClickedHandler() {
  _playVideoBinded();
}

/**
 * Handler for clicking of the close button.
 */
function _closeBtnClickedHandler() {
  _stopVideoBinded();
}

/**
 * Play the video.
 * @returns {VideoPlayer} An instance.
 */
function playVideo() {
  _player.playVideo();
  _dom.classList.add( 'video-playing' );
  this.dispatchEvent( 'onPlay' );

  return this;
}

/**
 * Stop the video from playing.
 * @returns {VideoPlayer} An instance.
 */
function stopVideo() {
  _player.stopVideo();
  _dom.classList.remove( 'video-playing' );
  this.dispatchEvent( 'onStop' );

  return this;
}

VideoPlayer.BASE_CLASS = BASE_CLASS;

export default VideoPlayer;
