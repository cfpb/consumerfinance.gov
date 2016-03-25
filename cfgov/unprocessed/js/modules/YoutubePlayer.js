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
  IFRAME_CLASS_NAME:     'video-player_iframe__youtube'
} );

var API = {

  constructor: YoutubePlayer,

  SCRIPT_API: 'http://www.youtube.com/iframe_api',

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
  },

  /**
   * Handle initializing of Youtube player and embed API script if necessary.
   */
  initPlayer: function( ) {
    var YouTubePlayer = window.YT;
    if ( YouTubePlayer && YouTubePlayer.Player ) {
      var player = new YouTubePlayer.Player( this.iFrameProperties.id
        , this.playerOptions );
      this.state.isPlayerInitialized = true;
    } else if( this.state.isScriptLoading === false ) {
      window.onYouTubeIframeAPIReady = this.initPlayer;
      this.embedScript();
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
    if( event.data === window.YT.PlayerState.ENDED ) {
      this.stop();
    }
  },

  /**
   * Action function used to play the Youtube video.
   */
  play: function( ) {
    this._super.play.call( this );
    if ( this.state.isPlayerInitialized ) {
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
    if ( this.player ) {
      this.player.stopVideo();
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
