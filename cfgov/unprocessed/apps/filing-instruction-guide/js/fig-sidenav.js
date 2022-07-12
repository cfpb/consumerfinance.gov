import Expandable from '@cfpb/cfpb-expandables/src/Expandable';


const appRoot = () => document.querySelector( 'main.o-fig' );

const getNavItem = target => appRoot().querySelector( `.m-nav-link[href="${ target }"]` );
const getNavItemContainer = target => getNavItem( target ).closest( '.o-secondary-navigation_list__children' ) || getNavItem( target ).nextElementSibling;

const highlightNavItem = target => getNavItem( target ).classList.add( 'm-nav-link__current' );
const unHighlightNavItem = target => getNavItem( target ).classList.remove( 'm-nav-link__current' );

const showElement = el => el && el.classList.remove( 'u-hide-on-desktop' );
const hideElement = el => el && el.classList.add( 'u-hide-on-desktop' );

let prevTarget;

/**
 * Description
 * @param {string} target - `href` value of the nav item to highlight
 */
const updateNav = target => {
  if ( target === prevTarget ) return;

  // Highlight the current nav item and expand its container if necessary
  const targetContainer = getNavItemContainer( target );
  showElement( targetContainer );
  highlightNavItem( target );

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
  // Only proceed if IntersectionObserver is supported (everything except IE)
  // See https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
  if ( 'IntersectionObserver' in window ) {
    appRoot().querySelectorAll( '.o-secondary-navigation_list__children' ).forEach( ul => {
      hideElement( ul );
    } );

    const observer = new IntersectionObserver( handleIntersect, {
      // Sets an intersection area that spans 5% above the top of the viewport and
      // 95% above the bottom of the viewport, resulting in a box that is 10% of
      // the viewport height with 5% hanging over the top.
      rootMargin: '5% 0px -95% 0px'
    } );

    const sections = appRoot().querySelectorAll( 'a[data-scrollspy]' );

    // Highlight the first section on page load
    updateNav( sections[0].getAttribute( 'href' ) );

    sections.forEach( section => observer.observe( section ) );
  }
};

Expandable.init();

window.addEventListener( 'load', init );
