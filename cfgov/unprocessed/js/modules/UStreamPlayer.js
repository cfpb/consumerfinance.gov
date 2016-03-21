'use strict';

var VideoPlayer = require( './VideoPlayer' );
var UStreamPlayer;

var CLASSES = Object.freeze( {
  VIDEO_PLAYER_SELECTOR: '.video-player__youtube',
  IFRAME_CLASS_NAME:     'video-player_iframe__youtube'
} );

var API = {

  SCRIPT_API: 'http://static.ustream.tv/js/libs/ustream-embedapi.min.js',

  constructor: UStreamPlayer,

  iFrameProperties: {
    id: CLASSES.IFRAME_CLASS_NAME
  },

  /**
   * Handle initializing of UStream player and embed API script if necessary.
   */
  initPlayer: function( ) {
    var UstreamPlayer = window.UstreamEmbed;
    if ( UstreamPlayer ) {
      this.player = new UstreamPlayer( this.iFrameProperties.id );
      this.initPlayerEvents();
      this.state.isPlayerInitialized = true;
    } else if( this.state.isScriptLoading === false ) {
      this.embedScript( this.SCRIPT_API, this.initPlayer.bind( this ) );
    }
  },

  /**
   * Handle initializing of Ustream player events.
   */
  initPlayerEvents: function() {
    this.player.addListener( 'finished', this.onLiveStreamEnded.bind( this ) );
  },

  /**
   * Callback function called when live stream has ended.
   */
  onLiveStreamEnded: function() {
    this.stop();
  },

  /**
   * Action function used to play the Ustream video.
   */
  play: function( ) {
    this._super.play.call( this );
    if ( this.state.isPlayerInitialized ) {
      this.player.callMethod( 'play' );
    } else {
      this.initPlayer();
    }
  },

  /**
   * Action function used to stop the Ustream video.
   */
  stop: function( ) {
    this._super.stop.call( this );
    if ( this.state.isPlayerInitialized ) {
      this.player.callMethod( 'stop' );
    }
  }
};


/**
 * UStreamPlayer
 * @class
 *
 * @classdesc Initializes a new UStream player.
 * Extends Video Player Class.
 *
 * @returns {UStreamPlayer} An instance.
 */
UStreamPlayer = VideoPlayer.extend( API );

// Expose public methods.
module.exports = UStreamPlayer;
