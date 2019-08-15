/* ==========================================================================
   Scripts for Video Player module.
   ========================================================================== */

import VideoPlayer from '../../organisms/VideoPlayer';

const videoPlayerDom = document.querySelector( `.${ VideoPlayer.BASE_CLASS }` );
const videoPlayer = new VideoPlayer( videoPlayerDom );
videoPlayer.init();
