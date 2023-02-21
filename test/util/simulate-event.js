/**
 * @param {string} eventType - The type of event.
 * @param {HTMLElement} target - Target of the event.
 * @param {object} eventOption - Options to add to the event.
 * @returns {HTMLElement} The target of the event.
 */
function simulateEvent(eventType, target, eventOption = {}) {
  let event;

  if (eventType === 'click') {
    event = new MouseEvent('click', {
      bubbles: true,
      cancelable: true,
      view: window,
    });
    // TODO: migrate to KeyBoardEvent, etc.
  } else {
    event = window.document.createEvent('Event', eventOption.currentTarget);
    event.initEvent(eventType, true, true);

    if (eventOption && eventOption.key) {
      event.key = eventOption.key;
    }
  }

  return target.dispatchEvent(event);
}

export { simulateEvent };
