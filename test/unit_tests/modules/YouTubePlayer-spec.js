'use strict';

var BASE_JS_PATH = '../../../cfgov/unprocessed/js/';
var chai = require( 'chai' );
var expect = chai.expect;
var jsdom = require( 'mocha-jsdom' );
var sinon = require( 'sinon' );
var YoutubePlayer = require( BASE_JS_PATH + 'modules/YoutubePlayer' );
var VideoPlayer = require( BASE_JS_PATH + 'modules/VideoPlayer' );
var sandbox;
var youtubePlayer;

var HTML_SNIPPET =
'<div class="video-player video-player__youtube"' +
  'data-id="V11Xbp9z2KQ"' +
  'data-src="https://www.youtube.com/embed/V11Xbp9z2KQ?autoplay=1&amp;enablejsapi=1&amp;origin=http://localhost:8000">' +
  '<div class="video-player_video-container show-on_video-playing">' +
    '<div class="video-player_iframe-container"></div>' +
      '<div class="video-player_video-actions-container">' +
        '<div class="video-player_video-actions">' +
          '<a class="btn video-player_close-btn" href="/">' +
              'close' +
           '</a>' +
        '</div>' +
      '</div>' +
  '</div>' +
  '<div class="video-player_image-container hide-on_video-playing">' +
    '<a class="video-player_play-btn"></a>' +
      '<img class="video-player_image" alt="Video image"' +
        'src="https://img.youtube.com/vi/V11Xbp9z2KQ/maxresdefault.jpg">' +
  '</div>' +
'</div>';

var YOUTUBE_STATES = {
  UNSTARTED: -1,
  ENDED:     0,
  PLAYING:   1,
  PAUSED:    2,
  BUFFERING: 3
};

describe( 'Youtube Player', function() {
  jsdom();

  beforeEach( function() {
    sandbox = sinon.sandbox.create();
    document.body.innerHTML = HTML_SNIPPET;
    var element = document.querySelector( '.video-player__youtube' );

    // Create mock Youtube dependencies.
    var YT = window.YT = {};
    YT.PlayerState = YOUTUBE_STATES;
    YT.Player = function Player() {};

    YT.setConfig = sinon.stub();
    youtubePlayer = new YoutubePlayer( element );
    youtubePlayer.player = {
      seekTo:   sinon.stub(),
      playVideo: sinon.stub(),
      stopVideo: sinon.stub()
    };
  } );

  afterEach( function() {
    sandbox.restore();
  } );

  it( 'should inherit from the Video Player',
    function() {
      expect( youtubePlayer instanceof VideoPlayer ).to.equal( true );
    }
  );

  it( 'init method should correctly set the instance properties',
    function() {
      expect( youtubePlayer instanceof VideoPlayer ).to.equal( true );
    }
  );

  it( 'initPlayer method should return a Youtube player instance',
    function() {
      var spy = sinon.spy( youtubePlayer, 'embedScript' );
      expect( youtubePlayer.initPlayer() instanceof window.YT.Player )
      .to.equal( true );

      // Delete player to test code branch.
      delete window.YT.Player;
      youtubePlayer.state.isScriptLoading = false;
      youtubePlayer.initPlayer();
      expect( spy.called ).to.equal( true );
      youtubePlayer.state.isScriptLoading = true;
      youtubePlayer.initPlayer();
      expect( typeof youtubePlayer.initPlayer() === 'undefined' )
      .to.equal( true );
    }
  );

  it( 'should modify its state correctly when the play method is invoked',
    function() {
      youtubePlayer.play();
      expect( youtubePlayer.state.getIsVideoPlaying() ).to.equal( true );
      expect( youtubePlayer.state.getIsVideoStopped() ).to.equal( false );
      youtubePlayer.state.isPlayerInitialized = false;
      youtubePlayer.play();
      expect( youtubePlayer.player.playVideo.called ).to.equal( true );
    }
  );

  it( 'should modify its state correctly when the stop method is invoked',
    function() {
      youtubePlayer.play();
      youtubePlayer.stop();
      expect( youtubePlayer.state.getIsVideoPlaying() ).to.equal( false );
      expect( youtubePlayer.state.getIsVideoStopped() ).to.equal( true );
      youtubePlayer.state.isPlayerInitialized = false;
      youtubePlayer.player.stopVideo.reset();
      youtubePlayer.stop();
      expect( youtubePlayer.player.stopVideo.called ).to.equal( false );
    }
  );

  it( 'should modify its state correctly when the onPlayerStateChange method is invoked',
    function() {
      youtubePlayer.play();
      expect( youtubePlayer.state.getIsVideoPlaying() ).to.equal( true );
      expect( youtubePlayer.state.getIsVideoStopped() ).to.equal( false );
      youtubePlayer.onPlayerStateChange( { data: YOUTUBE_STATES.ENDED } );
      expect( youtubePlayer.state.getIsVideoStopped() ).to.equal( true );
      expect( youtubePlayer.state.getIsVideoPlaying() ).to.equal( false );
      youtubePlayer.play();
      youtubePlayer.onPlayerStateChange( { data: YOUTUBE_STATES.PAUSED } );
      expect( youtubePlayer.state.getIsVideoStopped() ).to.equal( false );
    }
  );

  it( 'should set the player attribute when the onPlayerReady method is invoked',
    function() {
      var player = { target: {} };
      youtubePlayer.onPlayerReady( player );
      expect( Object.is( youtubePlayer.player, player.target ) )
      .to.equal( true );
      youtubePlayer.onPlayerReady();

      // Delete player to test code branch.
      delete youtubePlayer.player;
      youtubePlayer.onPlayerReady( {} );
      expect( typeof youtubePlayer.player === 'undefined' ).to.equal( true );
    }
  );
} );
