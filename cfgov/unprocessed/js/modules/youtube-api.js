/* ==========================================================================
   YouTube API
   ========================================================================== */

import jsLoader from './util/js-loader';

const IMAGE_URL = 'https://img.youtube.com/vi/%video_id%/maxresdefault.jpg';
const SCRIPT_API = 'https://www.youtube.com/iframe_api';

/**
 * The "onYouTubeIframeAPIReady" function is automatically called when the
 * YouTube IFrame API is done loading.
 * See https://developers.google.com/youtube/iframe_api_reference
 * @param {Function} callback - function to call when the API is ready.
 */
function attachAPIReadyCallback( callback ) {
  window.onYouTubeIframeAPIReady = callback;
}

/**
 * Embed the YouTube IFrame API.
 * @param {Function} [callback] - function to call when the script is loaded.
 */
function embedVideoScript( callback ) {
  jsLoader.loadScript( SCRIPT_API, callback );
}

/**
 * Load Youtube max res image if it exists.
 * TODO: Replace this method by calling the Youtube data API.
 * https://developers.google.com/youtube/v3/getting-started#fields
 */
/**
 * Load Youtube max res image if it exists.
 * TODO: Replace this method by calling the Youtube data API.
 *       https://developers.google.com/youtube/v3/getting-started#fields
 * @param {string} videoId - A YouTube video ID.
 * @returns {string} The image URL.
 */
function fetchImageURL( videoId ) {
  if ( !videoId ) {
    throw new Error( 'No Video ID provided!' );
  }

  return IMAGE_URL.replace( '%video_id%', videoId );
}

/**
 * Configure and load a new YouTube Player instance into a supplied <iframe>
 * from the YouTube embed API, which should have been set on the
 * global window object.
 *
 * @param {HTMLNode} iframeContainerDom -
 *   A reference to <iframe> to embed the video.
 * @param {string} videoId - A YouTube video ID.
 * @returns {YT.Player} A YouTube Player instance.
 * @throws {Error} If the IFrame API has not loaded.
 */
function instantiatePlayer( iframeContainerDom, videoId ) {
  if ( typeof window.YT === 'undefined' ) {
    throw new Error( 'YouTube IFrame API is not loaded!' );
  }

  const YouTubePlayer = window.YT;
  YouTubePlayer.setConfig( {
    host: 'https://www.youtube.com'
  } );

  const playerOptions = {
    videoId: videoId,
    playerVars: {
      autoplay: 1,
      enablejsapi: 1,
      origin: document.domain,
      rel: 0,
      suggestedQuality: 'highres'
    }
  };

  return new YouTubePlayer.Player( iframeContainerDom, playerOptions );
}

// Expose public methods.
export default {
  attachAPIReadyCallback,
  embedVideoScript,
  fetchImageURL,
  instantiatePlayer
};
