const videoPlayer = element( by.css( '.o-video-player' ) );

function _videoPlayerElement( selector ) {
  return videoPlayer.element( by.css( selector ) );
}

const VideoPlayer = {

  videoPlayerCloseButton: _videoPlayerElement( '.o-video-player_close-btn' ),

  videoPlayerVideoContainer:
    _videoPlayerElement( '.o-video-player_video-container' ),

  videoPlayerIframeContainer:
    _videoPlayerElement( '.o-video-player_iframe-container' ),

  getVideoPlayerIframe: function getVideoPlayerIframe() {
    return _videoPlayerElement( '.o-video-player_iframe' );
  },

  videoPlayerImageContainer:
    _videoPlayerElement( '.o-video-player_image-container' ),

  videoPlayerPlayButton: _videoPlayerElement( '.o-video-player_play-btn' ),

  videoPlayer: videoPlayer

};

module.exports = VideoPlayer;
