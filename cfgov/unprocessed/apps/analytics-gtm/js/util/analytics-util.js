import { analyticsLog } from '@cfpb/cfpb-analytics';

/**
 * Query a selector and add listeners to returned elements.
 * @param {string} selector - A dom selector.
 * @param {string} event - An event string, probably a "MouseEvent."
 * @param {Function} callback - The event handler.
 */
function addEventListenerToSelector(selector, event, callback) {
  const elems = document.querySelectorAll(selector);
  for (let i = 0, len = elems.length; i < len; i++) {
    addEventListenerToElem(elems[i], event, callback);
  }
}

/**
 * Check if an element exists on the page, and if it does, add listeners.
 * @param {HTMLElement} [elem] - The element to attach an event to.
 * @param {string} [event] - The event type string.
 * @param {Function} callback - Function to call when the event triggers.
 */
function addEventListenerToElem(elem, event, callback) {
  if (elem) {
    elem.addEventListener(event, callback);
  } else {
    analyticsLog(`${elem} doesn't exist!`);
  }
}

/**
 * Create a delay given a callback function and millisecond delay.
 * @class
 */
function Delay() {
  let timer = 0;
  return function (callback, ms) {
    clearTimeout(timer);
    timer = setTimeout(callback, ms);
  };
}

export { addEventListenerToSelector, addEventListenerToElem, Delay };
