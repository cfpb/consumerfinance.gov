let appRoot;
let navItems;
let navItemContainers;
let highlightNavItem;
let unHighlightNavItem;
let scrollNavItem;
let prevTarget;

/**
 * Initialize the side navigation variables.
 */
function init() {
  appRoot = document.querySelector('main.o-fig');
  navItems = appRoot.querySelectorAll('.o-secondary-nav__link[href]');

  navItems = Array.from(navItems).reduce(
    (map, navItem) => map.set(navItem.getAttribute('href'), navItem),
    new Map(),
  );

  navItemContainers = Array.from(navItems).reduce((map, [key, navItem]) => {
    const container =
      navItem.closest('.o-secondary-nav__list--children') ||
      navItem.nextElementSibling;
    return map.set(key, container);
  }, new Map());

  // TODO: Add these methods to SecondaryNav API to avoid adjusting
  // internal secondary nav state here.
  highlightNavItem = (target) =>
    navItems.get(target).classList.add('o-secondary-nav__link--current');

  unHighlightNavItem = (target) =>
    navItems.get(target).classList.remove('o-secondary-nav__link--current');

  scrollNavItem = (target) =>
    navItems.get(target).scrollIntoView({
      behavior: 'auto',
      block: 'nearest',
      inline: 'start',
    });
}

const showElement = (el) => el && el.classList.remove('u-hide-on-desktop');
const hideElement = (el) => el && el.classList.add('u-hide-on-desktop');

/**
 * The native scrollIntoView() function is great but when there's a sticky header,
 * the target element gets hidden underneath. This lets us specify an offset for
 * the target element to scroll to.
 * @param {HTMLElement} el - HTML element to scroll to.
 * @param {number} offset - number of pixels away from element.
 */
const scrollIntoViewWithOffset = (el, offset) => {
  window.scrollTo({
    top:
      el.getBoundingClientRect().top -
      document.body.getBoundingClientRect().top -
      offset,
    behavior: 'smooth',
  });
};

/**
 * Update the sidenav by highlighting the current section and showing
 * parent nav items as needed.
 * @param {string} target - `href` value of the nav item to highlight.
 */
const updateNav = (target) => {
  if (target === prevTarget) return;

  // Highlight the current nav item and expand its container if necessary.
  const targetContainer = navItemContainers.get(target);
  showElement(targetContainer);
  highlightNavItem(target);
  scrollNavItem(target);

  // Remove highlighting from the previous menu item and close its container.
  if (prevTarget) {
    unHighlightNavItem(prevTarget);
    const prevTargetContainer = navItemContainers.get(prevTarget);
    if (targetContainer !== prevTargetContainer) {
      hideElement(prevTargetContainer);
    }
  }

  prevTarget = target;
};

/**
 * Callback for IntersectionObserver
 * @param {IntersectionObserverEntry} entries - array of observer entries
 * See https://developer.mozilla.org/en-US/docs/Web/API/IntersectionObserverEntry
 */
/* Cypress tests cover IntersectionObserver behavior */
/* istanbul ignore next */
const handleIntersect = (entries) => {
  entries.forEach((entry) => {
    if (entry.intersectionRatio > 0) {
      updateNav('#' + entry.target.getAttribute('data-scrollspy'));
    }
  });
};

export {
  init,
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
  handleIntersect,
};
