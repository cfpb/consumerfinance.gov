import {
  addEventListenerToElem,
  track
} from './util/analytics-util';

const AccessibleInteractionsListeners = ( () => {

  // Listen for focus on the "skip link" button. This will grab the top link.
  const skipLinkButton = document.querySelector( '.skip-nav_link' );
  addEventListenerToElem( skipLinkButton, 'focus', () => {
    track( 'Accessibility Interactions', 'Focus', 'Skip link button' );
  } );
} )();
