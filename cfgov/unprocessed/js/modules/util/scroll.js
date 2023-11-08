/**
 * Easing.
 * @param {number} currentTime - current time.
 * @param {number} startPosition - start position.
 * @param {number} distance - difference between start and end position.
 * @param {number} duration - duration.
 * @returns {number} next position.
 */
function _easeInOutQuad(currentTime, startPosition, distance, duration) {
  let distanceDelta;
  const halfDuration = duration / 2;
  let updatedTime = currentTime / halfDuration;

  if (updatedTime < 1) {
    distanceDelta = (distance / 2) * updatedTime * updatedTime;
  } else {
    updatedTime--;
    distanceDelta = (-distance / 2) * (updatedTime * (updatedTime - 2) - 1);
  }
  return distanceDelta + startPosition;
}

/**
 * Calculate duration of scroll based on distance
 * @param {number} distance - The distance that will be scrolled
 * @returns {number} scroll duration
 */
function _calculateDuration(distance) {
  const duration = Math.abs(distance) / 2;
  return Math.min(Math.max(duration, 200), 1000) || 500;
}

/**
 * Animated scroll to a location in page.
 * @param {number} to - The y-coordinate to scroll to
 * @param {object} opts - Optional parameters, including:
 *    duration: Duration of the scroll animation
 *    callback: To be called when scroll is complete
 */
function scrollTo(to, opts) {
  opts = opts && typeof opts === 'object' ? opts : {};
  const startPosition = window.pageYOffset;
  const distance = to - startPosition;
  const duration = opts.duration || _calculateDuration(distance);
  let startTime;

  /**
   * Scroll the window for the duration
   * Trigger a callback after the duration has ended
   * @param {number} timestamp - the current time returned by
   *    requestAnimationFrame
   */
  function scroll(timestamp) {
    startTime = startTime || timestamp;
    const elapsed = timestamp - startTime;
    const next = _easeInOutQuad(elapsed, startPosition, distance, duration);
    window.scroll(0, next);

    if (elapsed < duration) {
      window.requestAnimationFrame(scroll);
    } else if (typeof opts.callback === 'function') {
      opts.callback();
    }
  }

  if (Math.abs(distance) > 3) {
    window.requestAnimationFrame(scroll);
  } else if (typeof opts.callback === 'function') {
    opts.callback();
  }
}

/**
 * Checks whether element in viewport and if not,
 * scrolls it into view.
 * @param {HTMLElement} elem - The DOM element to check for.
 * @param {object} opts - Optional parameters, including:
 *  offset: Distance from top of screen of element when scroll is complete.
 *  callback: function called when scroll is complete.
 */
function scrollIntoView(elem, opts) {
  const defaults = { offset: 15 };
  opts = Object.assign(defaults, opts);
  if (!elementInView(elem, true)) {
    const elementTop = elem.getBoundingClientRect().top;
    const to = Math.max(window.pageYOffset + elementTop - opts.offset, 0);
    scrollTo(to, opts);
  } else if (opts.callback && typeof opts.callback === 'function') {
    opts.callback();
  }
}

/**
 * @param {HTMLElement} elem - The DOM element to check for.
 * @param {boolean} strict - Tests whether whole element is
 *   onscreen rather than just a part.
 * @returns {boolean} Whether the element is in the viewport.
 */
function elementInView(elem, strict) {
  const windowHeight = window.innerHeight;
  const windowTop = window.pageYOffset;
  const windowBottom = windowTop + windowHeight;
  const elementHeight = elem.offsetHeight;
  const elementTop = elem.getBoundingClientRect().top + windowTop;
  const elementBottom = elementTop + elementHeight;

  if (strict) {
    return elementTop >= windowTop && elementBottom <= windowBottom;
  }
  return elementBottom >= windowTop && elementTop <= windowBottom;
}

window.scrollToElement = scrollTo;

export { elementInView, scrollIntoView, scrollTo };
