// TODO: remove jquery.
import $ from 'jquery';

/**
 * This function determines if the element specified is currently in the
 * browser window (i.e. "in view").
 * @param {string} selector - The selector for the element specified.
 * @returns {boolean} Whether or not the element is in the viewport.
 */
function isElementInView( selector ) {
  const $ele = $( selector );
  const target = $( window ).scrollTop() + $( window ).height() - 150;
  if ( $ele.offset().top > target ) {
    return false;
  }
  return true;
}

export default isElementInView;
