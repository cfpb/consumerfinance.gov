import {
  addEventListenerToElem,
  track
} from './util/analytics-util';

const AccessibleInteractionsListeners = ( () => {

  /* Listen for focus on the "skip link" button. This will grab the top link.
     Only the first link is needed since we're aiming to track users that use
     the tab-key from the get-go for navigation. */
  const skipLinkButton = document.querySelector( '.skip-nav_link' );
  addEventListenerToElem( skipLinkButton, 'focus', () => {
    track( 'Accessibility Interactions', 'Focus', 'Skip link button' );
  } );
} )();
