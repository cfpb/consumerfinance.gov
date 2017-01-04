/* ==========================================================================
   Youtube Player Class
   Extends Video Player Class.
   ========================================================================== */

'use strict';

var _noopFunct = require( './util/standard-type' ).noopFunct;
var VideoPlayer = require( './VideoPlayer' );
var YoutubePlayer;

var CLASSES = Object.freeze( {
  VIDEO_PLAYER_SELECTOR: '.video-player__youtube',
  IFRAME_CLASS_NAME:     'video-player_iframe__youtube',
  IMAGE_LOADED_STATE:    'video-player_image-loaded'
} );

var API = {

  constructor: YoutubePlayer,

  SCRIPT_API: 'https://www.youtube.com/iframe_api',

  IMAGE_URL: 'https://img.youtube.com/vi/%video_id%/maxresdefault.jpg',

  YOUTUBE_API_CONFIG: {
    host: 'https://www.youtube.com'
  },

  iFrameProperties: {
    id: CLASSES.IFRAME_CLASS_NAME
  },

  playerOptions: {
    videoId: '',
    playerVars: {
      autoplay: 1,
      suggestedQuality: 'highres'
    },
    events: {
      onReady: _noopFunct,
      onStateChange: _noopFunct
    }
  },

  /**
   * Adding Youtube player API callback listeners.
   */
  init: function( ) {
    var youtubeEvents = this.playerOptions.events;
    youtubeEvents.onReady = this.onPlayerReady.bind( this );
    youtubeEvents.onStateChange = this.onPlayerStateChange.bind( this );
    this.videoId = this.baseElement &&
      this.baseElement.getAttribute( 'data-id' );
    this.loadImage();
  },


  /**
   * Handle initializing of Youtube player and embed API script if necessary.
   * @returns {Object|undefined}
   *   YouTube player instance from the Google APIs or undefined if
   *   the Google APIs have not been loaded on the window object.
   */
  initPlayer: function( ) {
    var YouTubePlayer = window.YT;
    var player;
    if ( YouTubePlayer && YouTubePlayer.Player ) {
      YouTubePlayer.setConfig( this.YOUTUBE_API_CONFIG );
      player = new YouTubePlayer.Player( this.iFrameProperties.id
        , this.playerOptions );
      this.state.isPlayerInitialized = true;
    } else if ( this.state.isScriptLoading === false ) {
      window.onYouTubeIframeAPIReady = this.initPlayer.bind( this );
      this.embedScript();
    }

    return player;
  },

  /**
   * Load Youtube max res image if it exists.
   * TODO: Replace this method by calling the Youtube data API.
   * https://developers.google.com/youtube/v3/getting-started#fields
   */
  loadImage: function( ) {
    var defaultImage;
    var maxResImage;
    var maxResImageSrc;

    if ( this.videoId ) {
      defaultImage = this.childElements.image;
      maxResImage = document.createElement( 'img' );
      maxResImageSrc = this.IMAGE_URL.replace( '%video_id%', this.videoId );
      maxResImage.onload = onImageStateChange;
      maxResImage.onerror = onImageStateChange;
      maxResImage.src = maxResImageSrc;
    }

    /**
     * Event handler for loading state change (onload and onerror)
     * of an image element when the src attribute is set.
     */
    function onImageStateChange() {
      // 120px is the natural width of the default YouTube image.
      if ( maxResImage.naturalWidth && maxResImage.naturalWidth !== 120 ) {
        defaultImage.src = maxResImageSrc;
      }
      defaultImage.classList.add( CLASSES.IMAGE_LOADED_STATE );
    }
  },

   /**
   * Callback function called when Youtube player API
   * is loaded and events have been initialized.
   * @param {object} event - Youtube event data.
   */
  onPlayerReady: function( event ) {
    if ( event && event.target ) this.player = event.target;
  },

  /**
   * Callback function called when Youtube player state
   * has changed.
   * @param {object} event - Youtube event data.
   */
  onPlayerStateChange: function( event ) {
    if ( event.data === window.YT.PlayerState.ENDED ) {
      this.stop();
    }
  },

  /**
   * Action function used to play the Youtube video.
   */
  play: function( ) {
    this._super.play.call( this );
    if ( this.state.isPlayerInitialized && this.player ) {
      this.player.seekTo( 0 );
      this.player.playVideo();
    } else {
      this.initPlayer();
    }
  },

  /**
   * Action function used to play the Youtube video.
   */
  stop: function( ) {
    this._super.stop.call( this );
    if ( this.state.isPlayerInitialized && this.player ) {
      this.player.stopVideo();
    } else {
      this.childElements.iFrameContainer.removeChild(
        this.childElements.iFrameContainer.firstChild
      );
      this.state.setIsIframeLoaded( false );
    }
  }
};

/**
 * YoutubePlayer
 * @class
 *
 * @classdesc Initializes a new Youtube player.
 * Extends Video Player Class.
 *
 * @returns {YoutubePlayer} An instance.
 */
YoutubePlayer = VideoPlayer.extend( API );

// Expose public methods.
module.exports = YoutubePlayer;
