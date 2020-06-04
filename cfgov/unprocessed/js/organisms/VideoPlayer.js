/* ==========================================================================
   Video Player Class
   ========================================================================== */

// Required modules.
import { checkDom, setInitFlag } from '../modules/util/atomic-helpers';
import EventObserver from '../modules/util/EventObserver';
import youTubeAPI from '../modules/youtube-api';

const BASE_CLASS = 'o-video-player';

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
  const _dom = checkDom( element, BASE_CLASS );

  const _videoId = _dom.getAttribute( 'data-id' );
  const _showCustomThumbnail = _dom.hasAttribute( 'data-custom-thumbnail' );

  const _iframeDom = _dom.querySelector( `.${ BASE_CLASS }_iframe` );
  const _imageDom = _dom.querySelector( `.${ BASE_CLASS }_image` );
  const _closeBtnDom = _dom.querySelector( `.${ BASE_CLASS }_close-btn` );
  const _playBtnDom = _dom.querySelector( `button.${ BASE_CLASS }_play-btn` );
  const _playLinkDom = _dom.querySelector( `a.${ BASE_CLASS }_play-btn` );

  const _defaultThumbnailURL = _imageDom.src;

  // YouTube player object.
  let _player = null;

  /**
   * @returns {VideoPlayer|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function _init() {
    if ( !setInitFlag( _dom ) ) {
      let UNDEFINED;
      return UNDEFINED;
    }

    // Load a default thumbnail image if we're not using a custom one.
    if ( _videoId && !_showCustomThumbnail ) {
      _imageLoad( youTubeAPI.fetchImageURL( _videoId ) );
    }

    // Load the YouTube JS, triggering our callback.
    youTubeAPI.attachAPIReadyCallback( _videoAPIReady.bind( this ) );
    youTubeAPI.embedVideoScript();

    return this;
  }

  /**
   * Handler for when the video API has loaded and is ready, in this case when the
   * YouTube IFrame API is done loading.
   */
  function _videoAPIReady() {
    _player = youTubeAPI.instantiatePlayer( _iframeDom, _videoId );
    _player.addEventListener( 'onReady', _videoPlayerReadyHandler.bind( this ) );
    _player.addEventListener( 'onStateChange', _videoStateChangeHandler.bind( this ) );
  }

  /**
   * Event handler for the when the video is ready.
   */
  function _videoPlayerReadyHandler() {

    /* On page load we show a play link that links directly to the video, so
     * that the user can still access the video with no JavaScript. We need to
     * hide the link and show the play button for the embedded video. */
    _playLinkDom.classList.add( 'u-hidden' );
    _playBtnDom.classList.remove( 'u-hidden' );

    // Add events.
    _playBtnDom.addEventListener( 'click', _playBtnClickedHandler.bind( this ) );
    _closeBtnDom.addEventListener( 'click', _closeBtnClickedHandler.bind( this ) );

    // The video has loaded.
    _dom.classList.add( `${ BASE_CLASS }__loaded` );
  }

  /**
   * Handler for clicking of the play button.
   */
  function _playBtnClickedHandler() {
    this.playVideo();
  }

  /**
   * Handler for clicking of the close button.
   */
  function _closeBtnClickedHandler() {
    this.stopVideo();
  }

  /**
   * Handler for when the video changes state.
   * @param {Event} event - Event object for the changed state,
   *   which contains a data property for the state.
   */
  function _videoStateChangeHandler( event ) {
    if ( event.data === window.YT.PlayerState.ENDED ) {
      this.stopVideo();
    }
  }

  /**
   * Load Youtube max res image if it exists.
   * TODO: Replace this method by calling the YouTube data API.
   * https://developers.google.com/youtube/v3/getting-started#fields
   *
   * @param {string} imageURL - The URL to load in the image.
   */
  function _imageLoad( imageURL ) {
    _imageDom.addEventListener( 'load', _imageShow );
    _imageDom.addEventListener( 'error', _imageLoadDefault );

    _imageDom.src = imageURL;
  }

  /**
   * Show the image by adding a class that changes its opacity.
   */
  function _imageShow() {
    _imageDom.classList.add( `${ BASE_CLASS }_image-loaded` );
  }

  /**
   * Load the default image source (src) first set at load-time.
   */
  function _imageLoadDefault() {
    _imageDom.src = _defaultThumbnailURL;
  }

  /**
   * Play the video.
   * @returns {VideoPlayer} An instance.
   */
  function _playVideo() {
    if ( _player ) {
      _player.playVideo();
      _dom.classList.add( 'video-playing' );
      this.dispatchEvent( 'onPlay' );
    }

    return this;
  }

  /**
   * Stop the video from playing.
   * @returns {VideoPlayer} An instance.
   */
  function _stopVideo() {
    if ( _player ) {
      _player.stopVideo();
      _dom.classList.remove( 'video-playing' );
      this.dispatchEvent( 'onStop' );
    }

    return this;
  }

  // Attach public events.
  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.init = _init;
  this.playVideo = _playVideo;
  this.stopVideo = _stopVideo;

  return this;
}

VideoPlayer.BASE_CLASS = BASE_CLASS;

export default VideoPlayer;
