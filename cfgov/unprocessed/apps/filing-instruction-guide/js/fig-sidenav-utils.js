const appRoot = document.querySelector( 'main.o-fig' );

let navItems = appRoot.querySelectorAll( '.m-nav-link[href]' );
navItems = Array.from( navItems ).reduce(
  ( map, navItem ) => map.set( navItem.getAttribute( 'href' ), navItem ),
  new Map()
);

const navItemContainers = Array.from( navItems ).reduce(
  ( map, [ key, navItem ] ) => {
    const container =
      navItem.closest( '.o-secondary-navigation_list__children' ) ||
      navItem.nextElementSibling;
    return map.set( key, container );
  },
  new Map()
);

const highlightNavItem = target => navItems.get( target ).classList.add( 'm-nav-link__current' );
const unHighlightNavItem = target => navItems.get( target ).classList.remove( 'm-nav-link__current' );

const scrollNavItem = target => navItems.get( target ).scrollIntoView( {
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
 * @param {HTMLElement} el - HTML element to scroll to
 * @param {integer} offset - number of pixels away from element
 */
const scrollIntoViewWithOffset = ( el, offset ) => {
  window.scrollTo( {
    top:
      el.getBoundingClientRect().top -
      document.body.getBoundingClientRect().top -
      offset,
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
  const targetContainer = navItemContainers.get( target );
  showElement( targetContainer );
  highlightNavItem( target );
  scrollNavItem( target );

  // Remove the highlighting from the previous menu item and close its container
  if ( prevTarget ) {
    unHighlightNavItem( prevTarget );
    const prevTargetContainer = navItemContainers.get( prevTarget );
    if ( targetContainer !== prevTargetContainer ) {
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

export {
  appRoot,
  navItems,
  navItemContainers,
  highlightNavItem,
  unHighlightNavItem,
  scrollNavItem,
  showElement,
  hideElement,
  scrollIntoViewWithOffset,
  updateNav,
  handleIntersect
};
