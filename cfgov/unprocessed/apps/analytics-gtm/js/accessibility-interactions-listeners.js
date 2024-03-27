import { analyticsSendEvent } from '@cfpb/cfpb-analytics';
import { addEventListenerToElem } from './util/analytics-util';

(() => {
  /* Listen for focus on the "skip link" button. This will grab the top link.
     Only the first link is needed since we're aiming to track users that use
     the tab-key from the get-go for navigation. */
  const skipLinkButton = document.querySelector('.skip-nav__link');
  addEventListenerToElem(skipLinkButton, 'focus', () => {
    analyticsSendEvent({
      event: 'Accessibility Interactions',
      action: 'Focus',
      label: 'Skip link button',
    });
  });
})();
