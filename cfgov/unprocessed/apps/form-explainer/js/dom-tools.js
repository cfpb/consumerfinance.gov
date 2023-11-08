import fastDom from 'fastdom';

const NO_OP = () => {
  // Placeholder function meant to be overridden.
};

/**
 * Apply a function to one or more elements.
 * @param {HTMLElement|NodeList} elements - An HTML element or a list of them.
 * @param {Function} applyFn - A function to apply to the elements.
 * @returns {boolean} True if function was applied, false otherwise.
 */
function applyAll(elements, applyFn) {
  let parsedElements = elements;
  if (parsedElements instanceof HTMLElement) {
    parsedElements = [parsedElements];
  } else if (parsedElements instanceof NodeList) {
    parsedElements = Array.prototype.slice.call(elements);
  }

  if (parsedElements instanceof Array) {
    parsedElements.forEach(applyFn);
    return true;
  }

  return false;
}

/**
 * Bind a collection of events to a collection of elements.
 * @param {Array|string} elements - Collection of elements.
 * @param {Array | object} events - Collection of events.
 * @param {Function} callback - Function to call when events fire.
 */
function bindEvents(elements, events, callback = NO_OP) {
  if (Array.isArray(events) === false) {
    events = [events];
  }

  if (typeof elements === 'string') {
    elements = getEls(elements);
  }

  applyAll(elements, function (element) {
    events.forEach((event) => {
      element.addEventListener(event, callback);
    });
  });
}

/**
 * Creates and returns a div HTML element containing arbitrary HTML.
 * @param {string} HTML - Arbitrary HTML to include in created div.
 * @returns {HTMLElement} First HTMLElement in the created div.
 */
function createElement(HTML) {
  const div = document.createElement('div');
  div.innerHTML = HTML;

  return div.children[0];
}

/**
 * @param {string} selector - A DOM selector.
 * @param {string} className - A CSS class name.
 */
function removeClass(selector, className) {
  className = className.split(', ');

  applyAll(getEls(selector), (element) => {
    fastDom.mutate(() => element.classList.remove(...className));
  });
}

/**
 * @param {string} selector - A DOM selector.
 * @param {string} className - A CSS class name.
 */
function addClass(selector, className) {
  className = className.split(', ');

  applyAll(getEls(selector), (element) =>
    fastDom.mutate(() => element.classList.add(...className)),
  );
}

/**
 * @param {string} selector - A DOM selector.
 * @param {string} className - A CSS class name.
 * @returns {boolean} True if it contains the class, false otherwise.
 */
function hasClass(selector, className) {
  return getEl(selector).classList.contains(className);
}

/**
 * @param {string} selector - A DOM selector.
 * @returns {NodeList} List of retrieved elements.
 * TODO: This should have a conistent return type if possible.
 */
function getEls(selector) {
  if (_isEl(selector)) {
    return selector;
  }

  return document.querySelectorAll(selector);
}

/**
 * @param {string} selector - A DOM selector.
 * @returns {HTMLElement} The retrieved element.
 * TODO: This should have a conistent return type if possible.
 */
function getEl(selector) {
  if (_isEl(selector)) {
    return selector;
  }

  return document.querySelector(selector);
}

/**
 * @param {string} element - An HTML element.
 * @param {string} filter - Selector for matching on elements.
 * @returns {Array} List of previous elements.
 * TODO: This should have a conistent return type if possible.
 */
function getPreviousEls(element, filter = '*') {
  const previousSiblings = [];
  let prevEl = element.previousElementSibling;

  /**
   * @param {HTMLElement} el - An HTML element.
   * @returns {Function} The browser's Element.matches() method.
   */
  function _getMatches(el) {
    return (
      el.matches ||
      el.webkitMatchesSelector ||
      el.mozMatchesSelector ||
      el.msMatchesSelector
    );
  }
  const _matchesMethod = _getMatches(element);

  while (prevEl) {
    if (_matchesMethod.bind(prevEl)(filter)) {
      previousSiblings.push(prevEl);
    }
    prevEl = prevEl.previousElementSibling;
  }
  return previousSiblings;
}

/**
 * Check whether something is a NodeList, HTML element, or window.
 * @param {*} element - Something, possibly a list, element or window instance.
 * @returns {boolean} True if `element` meets the criteria, false otherwise.
 */
function _isEl(element) {
  return (
    element instanceof NodeList ||
    element instanceof HTMLElement ||
    element instanceof Window
  );
}

/**
 * Check whether something is a NodeList, HTML element, or window.
 * @param {*} selector - Something, possibly a list, element or window instance.
 */
function hide(selector) {
  applyAll(getEls(selector), (element) =>
    fastDom.mutate(() => (element.style.display = 'none')),
  );
}

/**
 * Check whether something is a NodeList, HTML element, or window.
 * @param {*} selector - Something, possibly a list, element or window instance.
 */
function show(selector) {
  applyAll(getEls(selector), (element) =>
    fastDom.mutate(() => (element.style.display = 'block')),
  );
}

/**
 * @param {HTMLElement} element - HTML element to adjust.
 * @param {number} time - When to call the callback.
 * @param {Function} [callback] - Function to call after delay.
 */
function fadeIn(element, time, callback = NO_OP) {
  element.style.transition = 'opacity ' + time + 'ms ease-in-out';
  element.style.opacity = 0.05;
  element.style.display = 'block';
  window.setTimeout(() => (element.style.opacity = 1), 100);
  window.setTimeout(() => callback(), time);
}

/**
 * @param {HTMLElement} element - HTML element to adjust.
 * @param {number} time - When to call the callback.
 * @param {Function} [callback] - Function to call after delay.
 */
function fadeOut(element, time, callback = NO_OP) {
  element.style.transition = 'opacity ' + time + 'ms ease-in-out';
  element.style.opacity = 1;
  window.setTimeout(() => (element.style.opacity = 0.05), 100);
  window.setTimeout(() => {
    element.style.display = 'none';
    return callback();
  }, time);
}

export default {
  applyAll,
  bindEvents,
  createElement,
  removeClass,
  addClass,
  hasClass,
  getEls,
  getEl,
  getPreviousEls,
  hide,
  show,
  fadeIn,
  fadeOut,
  mutate: fastDom.mutate.bind(fastDom),
  measure: fastDom.measure.bind(fastDom),
  nextFrame: fastDom.raf,
};
