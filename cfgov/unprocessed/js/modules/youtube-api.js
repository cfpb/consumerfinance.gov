/* ==========================================================================
   YouTube API
   ========================================================================== */

const IMAGE_URL = 'https://img.youtube.com/vi/%video_id%/maxresdefault.jpg';

let _callbacks;
let _scriptLoaded;

/**
 * Attach a callback to be called when the YouTube API is ready.
 * @param {Function} callback - function to call when the API is ready.
 */
function attachAPIReadyCallback(callback) {
  if (_scriptLoaded) {
    callback();
  }

  _callbacks = _callbacks || [];
  _callbacks.push(callback);

  /**
   * The "onYouTubeIframeAPIReady" function is automatically called when the
   * YouTube IFrame API is done loading.
   * See https://developers.google.com/youtube/iframe_api_reference
   */
  function onYouTubeIframeAPIReady() {
    _scriptLoaded = true;
    _callbacks.forEach((cb) => cb());
    _callbacks.splice(0);
  }

  window.onYouTubeIframeAPIReady = onYouTubeIframeAPIReady;
}

/**
 * Load Youtube max res image if it exists.
 * TODO: Replace this method by calling the Youtube data API.
 * https://developers.google.com/youtube/v3/getting-started#fields
 * @param {string} videoId - A YouTube video ID.
 * @returns {string} The image URL.
 */
function fetchImageURL(videoId) {
  if (!videoId) {
    throw new Error('No Video ID provided!');
  }

  return IMAGE_URL.replace('%video_id%', videoId);
}

/**
 * Configure and load a new YouTube Player instance into a supplied <iframe>
 * from the YouTube embed API, which should have been set on the
 * global window object.
 * @param {HTMLElement} iframeContainerDom - A reference to <iframe>
 *   to embed the video.
 * @param {string} videoId - A YouTube video ID.
 * @returns {object} A YouTube Player instance (YT.Player).
 * @throws {Error} If the IFrame API has not loaded.
 */
function instantiatePlayer(iframeContainerDom, videoId) {
  if (typeof window.YT === 'undefined') {
    throw new Error('YouTube IFrame API is not loaded!');
  }

  const YouTubePlayer = window.YT;
  YouTubePlayer.setConfig({
    host: 'https://www.youtube.com',
  });

  const playerOptions = {
    videoId: videoId,
    playerVars: {
      autoplay: 1,
      enablejsapi: 1,
      origin: document.domain,
      rel: 0,
      suggestedQuality: 'highres',
    },
  };

  return new YouTubePlayer.Player(iframeContainerDom, playerOptions);
}

// Expose public methods.
export default {
  attachAPIReadyCallback,
  fetchImageURL,
  instantiatePlayer,
};
