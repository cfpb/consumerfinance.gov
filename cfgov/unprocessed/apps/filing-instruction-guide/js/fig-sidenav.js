/* istanbul ignore file */
/* Cypress tests cover all the UI interactions on this page. */

import varsBreakpoints from '@cfpb/cfpb-core/src/vars-breakpoints.js';

import Expandable from '@cfpb/cfpb-expandables/src/Expandable.js';
import {
  DESKTOP,
  viewportIsIn,
} from '../../../js/modules/util/breakpoint-state.js';
import {
  init as figSidenavUtilsInit,
  appRoot,
  hideElement,
  handleIntersect,
  scrollIntoViewWithOffset,
} from './fig-sidenav-utils.js';

/**
 * Default scroll into view with an 60 pixel offset.
 */
const defaultScrollOffset = (target) => {
  scrollIntoViewWithOffset(
    document.getElementById(target.getAttribute('href').replace('#', '')),
    60
  );
};

/**
 * The sidenav is nested inside an expandable on smaller screens.
 * We have to close the expandable before sending the user to the appropriate section.
 *
 * @param {MouseEvent} event - Event from user clicking/tapping a nav item.
 */
const handleMobileNav = (event) => {
  event.preventDefault();
  if (event.target.matches('.m-nav-link')) {
    document.querySelector('.o-fig_sidebar .o-expandable_header').click();
    // Scrolling before the expandable closes causes jitters on some devices.
    setTimeout(() => {
      defaultScrollOffset(event.target);
    }, 300);
  } else if (event.target.matches('.o-fig_heading > a')) {
    defaultScrollOffset(event.target);
  }
};

/**
 * init - Initialize everything on page load.
 */
const init = () => {
  figSidenavUtilsInit();

  /* If the browser window is no greater than 900px, enable the mobile nav
   functionality. Otherwise, disable it. This event is triggered whenever
   the user resizes the viewport and its width passes the 900px threshold. */
  window
    .matchMedia(`(max-width: ${varsBreakpoints.bpSM.max}px)`)
    .addEventListener('change', (mediaQuery) => {
      if (mediaQuery.matches) {
        appRoot.addEventListener('click', handleMobileNav);
      } else {
        appRoot.removeEventListener('click', handleMobileNav);
      }
    });

  Expandable.init();

  /* Only proceed if IntersectionObserver is supported (everything except IE)
     See https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API */
  if ('IntersectionObserver' in window) {
    appRoot
      .querySelectorAll('.o-secondary-navigation_list__children')
      .forEach((ul) => {
        hideElement(ul);
      });

    const observer = new IntersectionObserver(handleIntersect, {
      root: document,

      /* Sets an intersection area that spans 5% above the top of the viewport and
         5% above the bottom of the viewport, resulting in a box that is 30% of
         the viewport height with 5% hanging over the top. */
      rootMargin: '5% 0px -75% 0px',
    });

    const sections = appRoot.querySelectorAll('[data-scrollspy]');

    sections.forEach((section) => observer.observe(section));
  }

  if (!viewportIsIn(DESKTOP)) {
    appRoot.addEventListener('click', handleMobileNav);
  }
};

export { init };
