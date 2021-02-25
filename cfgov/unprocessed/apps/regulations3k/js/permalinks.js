/**
 * To auto update the URL's hash as users scroll through regs, we populate an
 * array of objects that maps every paragraph's ID to its Y coordinate on page
 * load. We regenerate this array if the user resizes the window or clicks on
 * an expandable (because both those actions cause paragraphs to move around
 * the page).
 *
 * As users scroll through the page we search the array for the paragraph
 * closest to the top of the viewport and update the URL hash accordingly.
 *
 * The wayfinder element uses the same paragraph IDs (and data-label) to
 * populate its description.
 */

import {
  debounce,
  updateParagraphPositions,
  updateUrlHash,
  updateWayfinder
} from './permalinks-utils';
import { queryOne as find } from '@cfpb/cfpb-atomic-component/src/utilities/dom-traverse.js';

const wayfinderLink = find( '.o-regulations-wayfinder_link' );

/**
 * init - Initialize the permalink functionality by cataloging all paragraph
 * locations and adding event listeneres for re-cataloging when necessary.
 */
const init = () => {
  updateParagraphPositions();
  updateWayfinder( true );
  if ( wayfinderLink !== null ) {
    wayfinderLink.addEventListener( 'click', event => {
      event.preventDefault();
      updateWayfinder( true );
    } );
  }

  debounce( 'resize', 300, updateParagraphPositions );
  debounce( 'click', 300, updateParagraphPositions );
  debounce( 'scroll', 100, updateUrlHash );
  debounce( 'scroll', 100, updateWayfinder );

};

// Provide the no-JS experience to browsers without `replaceState`
if ( 'replaceState' in window.history ) {
  window.addEventListener( 'load', init );
}
