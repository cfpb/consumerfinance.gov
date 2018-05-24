const videoPlayer = element( by.css( '.video-player' ) );

function _videoPlayerElement( selector ) {
  return videoPlayer.element( by.css( selector ) );
}

const VideoPlayer = {

  videoPlayerCloseButton: _videoPlayerElement( '.video-player_close-btn' ),

  videoPlayerVideoContainer:
    _videoPlayerElement( '.video-player_video-container' ),

  videoPlayerIframeContainer:
    _videoPlayerElement( '.video-player_iframe-container' ),

  getVideoPlayerIframe: function getVideoPlayerIframe() {
    return _videoPlayerElement( '.video-player_iframe' );
  },

  videoPlayerImageContainer:
    _videoPlayerElement( '.video-player_image-container' ),

  videoPlayerPlayButton: _videoPlayerElement( '.video-player_play-btn' ),

  videoPlayer: videoPlayer

};

module.exports = VideoPlayer;
