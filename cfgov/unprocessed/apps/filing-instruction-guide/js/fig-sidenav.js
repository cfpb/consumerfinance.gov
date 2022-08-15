import Expandable from '@cfpb/cfpb-expandables/src/Expandable';
import { DESKTOP, viewportIsIn } from '../../../js/modules/util/breakpoint-state.js';
import * as fig from './fig-sidenav-utils';

/**
 * init - Initialize everything on page load.
 */
const init = () => {
  /* Only proceed if IntersectionObserver is supported (everything except IE)
     and we're on a larger screen
     See https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API */
  if ( 'IntersectionObserver' in window && viewportIsIn( DESKTOP ) ) {
    fig.appRoot.querySelectorAll( '.o-secondary-navigation_list__children' ).forEach( ul => {
      fig.hideElement( ul );
    } );

    const observer = new IntersectionObserver( fig.handleIntersect, {
      root: document,

      /* Sets an intersection area that spans 5% above the top of the viewport and
         95% above the bottom of the viewport, resulting in a box that is 10% of
         the viewport height with 5% hanging over the top. */
      rootMargin: '5% 0px -95% 0px'
    } );

    const sections = fig.appRoot.querySelectorAll( 'a[data-scrollspy]' );

    // Highlight the first section on page load
    fig.updateNav( sections[0].getAttribute( 'href' ) );

    sections.forEach( section => observer.observe( section ) );
  }

  if ( !viewportIsIn( DESKTOP ) ) {
    fig.appRoot.addEventListener( 'click', event => {
      if ( event.target.matches( '.m-nav-link' ) ) {
        event.preventDefault();
        document.querySelector( '.o-fig_sidebar .o-expandable_header' ).click();
        // Scrolling before the expandable closes causes jitters on some devices
        setTimeout( () => {
          fig.scrollIntoViewWithOffset( document.getElementById( event.target.getAttribute( 'href' ).replace( '#', '' ) ), 60 );
        }, 300 );
      }
      if ( event.target.matches( '.o-fig_heading > a' ) ) {
        event.preventDefault();
        fig.scrollIntoViewWithOffset( document.getElementById( event.target.getAttribute( 'href' ).replace( '#', '' ) ), 60 );
      }
    } );
  }
};

Expandable.init();

init();
