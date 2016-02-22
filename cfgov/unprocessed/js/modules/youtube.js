/* ==========================================================================
   YouTube Initialization
   Used on at least `/the-bureau/`.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
var jsLoader = require( './util/js-loader' );

/**
 * Set up jQuery plugin initialization.
 * @returns {Object} jQuery object.
 */
function init() {

  /**
  * Create the jQuery YouTube plugin.
  * @param {object} options Object used to customize YouTube.
  * @returns {object} jQuery element.
  */
  $.fn.createYouTube = function( options ) {
    options = $.extend( true, {}, this.data(), options );

    return this.each( function() {
      $( this ).data( 'plugin', new YouTube( this, options ) );
    } );
  };

  return $( '.video-player__youtube' ).createYouTube();
}

/**
* TODO: Move YouTube "class" to its own YouTube.js module.
* YouTube constructor.
* @class
* @param {HTMLElement} element DOM Element.
* @param {object} options Object used to customize YouTube.
*/
function YouTube( element, options ) {
  var playerOptions = this.defaults.playerOptions;
  this.$element = $( element );
  $.extend( true, playerOptions, options );
  this.init();
}

// YouTube methods and shared properties
YouTube.prototype = {

  constructor: YouTube,

  defaults: {
    playerOptions: {
      videoId:    '',
      playerVars: {
        autoplay:         1,
        suggestedQuality: 'highres'
      },
      events: {
        onReady:       $.noop,
        onStateChange: $.noop
      }
    },
    playerInitialized: false
  },

  _bindAll: function() {
    var self = this;
    var proxy = $.proxy;

    // TODO: Swap this out for Function.bind
    // and Object.keys.
    $.each( this, function( key, _function ) {
      if ( $.isFunction( _function ) ) {
        self[key] = proxy( _function, self );
      }
    } );

    return this;
  },

  _embedScript: function() {
    window.onYouTubeIframeAPIReady = this.initPlayer;
    jsLoader.loadScript( 'http://www.youtube.com/iframe_api' );

    return this;
  },

  init: function() {
    this._bindAll();
    this.initUI();

    var YouTubeEvents = this.defaults.playerOptions.events;
    YouTubeEvents.onReady = this.onPlayerReady;
    YouTubeEvents.onStateChange = this.onPlayerStateChange;

    return this;
  },

  initUI: function() {
    var ui = this.$element;
    ui.on( 'click', '.video-player_play-btn', this.play );
    ui.on( 'click', '.video-player_close-btn', this.close );

    return this;
  },

  destroy: function() {
    var self = this;
    this.$element.remove();

    $.each( this, function( key ) {
      delete self[key];
    }, this );

    return this;
  },

  initPlayer: function() {
    var YT = window.YT;
    if ( YT && YT.Player ) {
      new YT.Player( 'youtube_video-player', this.defaults.playerOptions );
      this.playerInitialized = true;
    } else {
      this._embedScript();
    }

    return this;
  },

  onPlayerStateChange: function( event ) {
    if ( event.data === window.YT.PlayerState.ENDED ) {
      this.$element.removeClass( 'video-playing' );
    }

    return this;
  },

  onPlayerReady: function( params ) {
    if ( params && params.target ) {
      this.player = params.target;
    }
  },

  play: function( event ) {
    event.preventDefault();
    event.stopImmediatePropagation();
    if ( this.playerInitialized ) {
      this.player.seekTo( 0 );
      this.player.playVideo();
    } else {
      this.initPlayer();
    }
    this.$element.addClass( 'video-playing' );

    return this;
  },

  close: function( event ) {
    event.preventDefault();
    this.player.stopVideo();
    this.$element.removeClass( 'video-playing' );

    return this;
  },

  show: function() {
    this.$element.slideDown( {
      easing: this.defaults.easing
    } );

    return this;
  },

  hide: function() {
    this.$element.slideUp( {
      easing: this.defaults.easing
    } );

    return this;
  }
};

// Expose public methods.
module.exports = { init: init };
