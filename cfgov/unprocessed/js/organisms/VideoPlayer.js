/* ==========================================================================
   Video Player Class
   ========================================================================== */

// Required modules.
import {
  checkDom,
  setInitFlag
} from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import { formatTimestamp } from '../modules/util/strings.js';
import EventObserver from '@cfpb/cfpb-atomic-component/src/mixins/EventObserver.js';
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
  const _closeBtnDom = _dom.querySelector( `button.${ BASE_CLASS }_close-btn` );
  const _playBtnDom = _dom.querySelector( `button.${ BASE_CLASS }_play-btn` );
  const _playLinkDom = _dom.querySelector( `a.${ BASE_CLASS }_play-btn` );
  const _durationDom = _dom.querySelector( `.${ BASE_CLASS }_duration` );

  const _defaultThumbnailURL = _imageDom.src;

  // YouTube player object.
  let _player = null;

  /**
   * @returns {VideoPlayer|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !setInitFlag( _dom ) ) {
      let UNDEFINED;
      return UNDEFINED;
    }

    // Load the thumbnail from YouTube if we haven't specified one in the DOM.
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
   * Event handler for when the video is ready.
   * @param {Object} event -
   *   Event object containing target to video player instance.
   */
  function _videoPlayerReadyHandler( event ) {
    // Add duration timestamp to video.
    const player = event.target;
    const duration = player.getDuration();
    _durationDom.setAttribute( 'datetime', duration + 'S' );
    _durationDom.innerHTML = formatTimestamp( duration );
    _durationDom.classList.remove( 'u-hidden' );

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
    _imageDom.addEventListener( 'load', _imageLoaded );
    _imageDom.addEventListener( 'error', _imageLoadFailed );

    _imageDom.src = imageURL;
  }

  /**
   * Error handler for thumbnail image loading.
   * If for some reason we can't load the specified thumbnail image, we
   * should try to load the default thumbnail. But don't do that if we've
   * already tried and failed to do so once.
   */
  function _imageLoadFailed() {
    if ( _imageDom.src === _defaultThumbnailURL ) {
      _imageLoadDefault();
    }
  }

  /**
   * Event handler for when image src attribute is set.
   */
  function _imageLoaded() {
    /* 120px is the natural width of the default YouTube image.
     * This condition will be true when there isn't a custom image set. */
    if ( _imageDom.naturalWidth === 120 ) {
      _imageLoadDefault();
    }

    _imageShow();
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
  function playVideo() {
    if ( _player ) {
      _player.playVideo();
      _dom.classList.add( 'video-playing' );

      /* Allow keyboard navigation of the close button and video iframe.
       * Disallow keyboard navigation of the play button. */
      _closeBtnDom.removeAttribute( 'tabindex' );
      _iframeDom.removeAttribute( 'tabindex' );
      _playBtnDom.setAttribute( 'tabindex', '-1' );

      // Set the keyboard focus to the close button.
      _closeBtnDom.focus();

      this.dispatchEvent( 'onPlay' );
    }

    return this;
  }

  /**
   * Stop the video from playing.
   * @returns {VideoPlayer} An instance.
   */
  function stopVideo() {
    if ( _player ) {
      _player.stopVideo();
      _dom.classList.remove( 'video-playing' );

      /* Allow keyboard navigation of the play button.
       * Disallow keyboard navigation of the close button and video iframe. */
      _closeBtnDom.setAttribute( 'tabindex', '-1' );
      _iframeDom.setAttribute( 'tabindex', '-1' );
      _playBtnDom.removeAttribute( 'tabindex' );

      // Set the keyboard focus to the play button.
      _playBtnDom.focus();

      this.dispatchEvent( 'onStop' );
    }

    return this;
  }

  // Attach public events.
  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.init = init;
  this.playVideo = playVideo;
  this.stopVideo = stopVideo;

  return this;
}

VideoPlayer.BASE_CLASS = BASE_CLASS;

export default VideoPlayer;
