export class VideoPlayer {

  videoPlayer() {
    return cy.get( '.o-video-player' );
  }

  videoPlayerElement( selector ) {
    return this.videoPlayer().get( selector );
  }

  videoPlayerIframe() {
    return this.videoPlayerElement( '.o-video-player_iframe' );
  }

  videoPlayerCloseButton() {
    return this.videoPlayerElement( '.o-video-player_close-btn' );
  }

  videoPlayerPlayButton() {
    return this.videoPlayerElement( '.o-video-player_play-btn' );
  }

  videoPlayerIframeContainer() {
    return this.videoPlayerElement( '.o-video-player_iframe-container' );
  }

  videoPlayerImageContainer() {
    return this.videoPlayerElement( '.o-video-player_image-container' );
  }

  videoPlayerVideoContainer() {
    return this.videoPlayerElement( '.o-video-player_video-container' );
  }
}
