/* istanbul ignore file */
/* Cypress tests cover all the UI interactions on this page. */

import varsBreakpoints from '@cfpb/cfpb-core/src/vars-breakpoints';

import Expandable from '@cfpb/cfpb-expandables/src/Expandable';
import {
  DESKTOP,
  viewportIsIn,
} from '../../../js/modules/util/breakpoint-state.js';
import * as fig from './fig-sidenav-utils';

/**
 * The sidenav is nested inside an expandable on smaller screens.
 * We have to close the expandable before sending the user to the appropriate section.
 *
 * @param {MouseEvent} event - Event from user clicking/tapping a nav item
 */
const handleMobileNav = (event) => {
  if (event.target.matches('.m-nav-link')) {
    event.preventDefault();
    document.querySelector('.o-fig_sidebar .o-expandable_header').click();
    // Scrolling before the expandable closes causes jitters on some devices
    setTimeout(() => {
      fig.scrollIntoViewWithOffset(
        document.getElementById(
          event.target.getAttribute('href').replace('#', '')
        ),
        60
      );
    }, 300);
  }
  if (event.target.matches('.o-fig_heading > a')) {
    event.preventDefault();
    fig.scrollIntoViewWithOffset(
      document.getElementById(
        event.target.getAttribute('href').replace('#', '')
      ),
      60
    );
  }
};

/**
 * init - Initialize everything on page load.
 */
const init = () => {
  /* Only proceed if IntersectionObserver is supported (everything except IE)
     See https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API */
  if ('IntersectionObserver' in window) {
    fig.appRoot
      .querySelectorAll('.o-secondary-navigation_list__children')
      .forEach((ul) => {
        fig.hideElement(ul);
      });

    const observer = new IntersectionObserver(fig.handleIntersect, {
      root: document,

      /* Sets an intersection area that spans 5% above the top of the viewport and
         95% above the bottom of the viewport, resulting in a box that is 10% of
         the viewport height with 5% hanging over the top. */
      rootMargin: '5% 0px -95% 0px',
    });

    const sections = fig.appRoot.querySelectorAll('a[data-scrollspy]');

    sections.forEach((section) => observer.observe(section));
  }

  if (!viewportIsIn(DESKTOP)) {
    fig.appRoot.addEventListener('click', handleMobileNav);
  }
};

/* If the browser window is no greater than 900px, enable the mobile nav
   functionality. Otherwise, disable it. This event is triggered whenever
   the user resizes the viewport and its width passes the 900px threshold. */
window
  .matchMedia(`(max-width: ${varsBreakpoints.bpSM.max}px)`)
  .addEventListener('change', (mediaQuery) => {
    if (mediaQuery.matches) {
      fig.appRoot.addEventListener('click', handleMobileNav);
    } else {
      fig.appRoot.removeEventListener('click', handleMobileNav);
    }
  });

Expandable.init();

init();
