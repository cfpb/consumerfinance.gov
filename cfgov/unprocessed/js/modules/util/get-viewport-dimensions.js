/* ==========================================================================
   Get Viewport Dimensions
   ========================================================================== */

/**
 * @returns {object} An object literal with the viewport
 *   width and height as properties.
 */
function getViewportDimensions() {

  /* TODO: Check what browsers this is necessary for and
     check whether it is still applicable. */
  let viewportEl = window;
  let propPrefix = 'inner';
  const modernBrowser = 'innerWidth' in window;
  if ( !modernBrowser ) {
    viewportEl = document.documentElement || document.body;
    propPrefix = 'client';
  }

  return {
    width:  viewportEl[propPrefix + 'Width'],
    height: viewportEl[propPrefix + 'Height']
  };
}

// Expose public methods.
export {
  getViewportDimensions
};
