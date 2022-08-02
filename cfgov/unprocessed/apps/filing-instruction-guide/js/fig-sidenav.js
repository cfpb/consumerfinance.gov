import Expandable from '@cfpb/cfpb-expandables/src/Expandable';
import { DESKTOP, viewportIsIn } from '../../../js/modules/util/breakpoint-state.js';

const appRoot = () => document.querySelector( 'main.o-fig' );

const getNavItem = target => appRoot().querySelector( `.m-nav-link[href="${ target }"]` );
const getNavItemContainer = target => getNavItem( target ).closest( '.o-secondary-navigation_list__children' ) || getNavItem( target ).nextElementSibling;

const highlightNavItem = target => getNavItem( target ).classList.add( 'm-nav-link__current' );
const unHighlightNavItem = target => getNavItem( target ).classList.remove( 'm-nav-link__current' );

const scrollNavItem = target => getNavItem( target ).scrollIntoView( {
  behavior: 'auto',
  block: 'nearest',
  inline: 'start'
} );

const showElement = el => el && el.classList.remove( 'u-hide-on-desktop' );
const hideElement = el => el && el.classList.add( 'u-hide-on-desktop' );

let prevTarget;

/**
 * The native scrollIntoView() function is great but when there's a sticky header,
 * the target element gets hidden underneath. This lets us specify an offset for
 * the target element to scroll to.
 * @param {DOMNode} el - HTML element to scroll to
 * @param {integer} offset - number of pixels away from element
 */
const scrollIntoViewWithOffset = ( el, offset ) => {
  window.scrollTo( {
    top: el.getBoundingClientRect().top - document.body.getBoundingClientRect().top - offset,
    behavior: 'smooth'
  } );
};

/**
 * Update the sidenav by highlighting the current section and showing
 * parent nav items as needed
 * @param {string} target - `href` value of the nav item to highlight
 */
const updateNav = target => {
  if ( target === prevTarget ) return;

  // Highlight the current nav item and expand its container if necessary
  const targetContainer = getNavItemContainer( target );
  showElement( targetContainer );
  highlightNavItem( target );
  scrollNavItem( target );

  // Remove the highlighting from the previous menu item and close its container
  if ( prevTarget ) {
    unHighlightNavItem( prevTarget );
    const prevTargetContainer = getNavItemContainer( prevTarget );
    if ( prevTargetContainer !== targetContainer ) {
      hideElement( prevTargetContainer );
    }
  }

  prevTarget = target;
};

/**
 * Callback for IntersectionObserver
 * @param {IntersectionObserverEntry} entries - array of observer entries
 * See https://developer.mozilla.org/en-US/docs/Web/API/IntersectionObserverEntry
 */
const handleIntersect = entries => {
  entries.forEach( entry => {
    if ( entry.intersectionRatio > 0 ) {
      updateNav( entry.target.getAttribute( 'href' ) );
    }
  } );
};

/**
 * init - Initialize everything on page load.
 */
const init = () => {
  /* Only proceed if IntersectionObserver is supported (everything except IE)
     and we're on a larger screen
     See https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API */
  if ( 'IntersectionObserver' in window && viewportIsIn( DESKTOP ) ) {
    appRoot().querySelectorAll( '.o-secondary-navigation_list__children' ).forEach( ul => {
      hideElement( ul );
    } );

    const observer = new IntersectionObserver( handleIntersect, {
      root: document,

      /* Sets an intersection area that spans 5% above the top of the viewport and
         95% above the bottom of the viewport, resulting in a box that is 10% of
         the viewport height with 5% hanging over the top. */
      rootMargin: '5% 0px -95% 0px'
    } );

    const sections = appRoot().querySelectorAll( 'a[data-scrollspy]' );

    // Highlight the first section on page load
    updateNav( sections[0].getAttribute( 'href' ) );

    sections.forEach( section => observer.observe( section ) );
  }

  if ( !viewportIsIn( DESKTOP ) ) {
    appRoot().addEventListener( 'click', event => {
      if ( event.target.classList.contains( 'm-nav-link' ) ) {
        event.preventDefault();
        document.querySelector( '.o-fig_sidebar .o-expandable_header' ).click();
        // Scrolling before the expandable closes causes jitters on some devices
        setTimeout( () => {
          scrollIntoViewWithOffset( document.getElementById( event.target.getAttribute( 'href' ).replace( '#', '' ) ), 60 );
        }, 300 );
      }
    } );
  }
};

Expandable.init();

init();
