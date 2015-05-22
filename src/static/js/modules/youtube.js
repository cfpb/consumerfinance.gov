/* ==========================================================================
   YouTube Initialization
   Used on at least `/the-bureau/`.
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
var jsLoader = require( './util/js-loader' );
var utilities = require( './util/utilities' );
var _viewportWidth = utilities.getViewportDimensions().width;

function init() {
  // Create the jQuery YouTube plugin.
  // @param {Object} Object used to customize YouTube.
  // @returns jQuery element.
  $.fn.createYouTube = function( options ) {
    options = $.extend( true, {}, this.data(), options );

    return this.each( function() {
      $( this ).data( 'plugin', new YouTube( this, options ) );
    } );
  };

  return $( '.youtube-player_container' ).createYouTube();
}

// YouTube constructor.
// @param element {Element} DOM Element.
// @param options {Object} Object used to customize YouTube.
// @returns {Object} An YouTube instance.
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
      height:     '410',
      width:      '640',
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
    ui.on( 'click', '.youtube-player_play-btn', this.play );
    ui.on( 'click', '.youtube-player_close-btn', this.close );

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
      new YT.Player( 'youtube-player', this.defaults.playerOptions );
      this.playerInitialized = true;
    } else {
      this._embedScript();
    }

    return this;
  },

  onPlayerStateChange: function( event ) {
    if ( event.data === window.YT.PlayerState.ENDED ) {
      this.$element.removeClass( 'yt-playing' );
    }

    return this;
  },

  onPlayerReady: function( params ) {
    if ( params && params.target ) {
      this.player = params.target;
    }
  },

  play: function( e ) {
    e.preventDefault();
    if ( this.playerInitialized ) {
      this.player.seekTo( 0 );
      this.player.playVideo();
    } else {
      this.initPlayer();
    }
    this.$element.addClass( 'yt-playing' );

    if ( _viewportWidth <= 800 ) {
      $( 'html, body' ).animate( { scrollTop: 0 }, 500 );
    }

    return this;
  },

  close: function( e ) {
    e.preventDefault();
    this.player.stopVideo();
    this.$element.removeClass( 'yt-playing' );

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
