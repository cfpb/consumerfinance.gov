/* ==========================================================================
   Scripts for Expandable Group organism.
   ========================================================================== */

import {
  addEventListenerToSelector,
  analyticsLog,
  removeEventListenerFromSelector
} from '../../../apps/analytics-gtm/js/util/analytics-util';

import Expandable from 'cf-expandables/src/Expandable';
Expandable.init();


/**
 * Tells Mouseflow to stop capturing, if it already is, and start a new capture.
 */
function stopStartMouseflow() {
  console.log( 'stopStartMouseflow' );
  if ( window.mouseflow ) {
    // Stop any in-progress heatmap capturing.
    window.mouseflow.stop();
    // Start a new heatmap recording.
    window.mouseflow.start();
    analyticsLog( 'Mouseflow capture started!' );
  }
}

/**
 * @param {MouseEvent} event - Mouse event from the click.
 */
function handleExpandable() {
  console.log( 'handleExpandable' );
  removeEventListenerFromSelector(
    Expandable.prototype.ui.target,
    'click',
    handleExpandable
  );
  const waitForTransition = window.setTimeout( stopStartMouseflow, 500 );
}

addEventListenerToSelector(
  Expandable.prototype.ui.target,
  'click',
  handleExpandable
);
