import {
  addEventListenerToElem,
  track
} from './util/analytics-util';

const AccessibleInteractionsListeners = ( function() {

  // Listen for focus on the "skip link" button.
  const skipLinkButton = document.querySelector( '#skip-nav' );
  addEventListenerToElem( skipLinkButton, 'focus', () => {
    track( 'Accessibility Interactions', 'Focus', 'Skip link button' );
  } );
} )();
