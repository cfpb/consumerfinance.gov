/**
 * @param {string} eventType - The type of event.
 * @param {HTMLElement} target - Target of the event.
 * @param {object} eventOption - Options to add to the event.
 * @returns {HTMLElement} The target of the event.
 */
function simulateEvent(eventType, target, eventOption = {}) {
  let event;

  // Add more event types here as required by tests.
  switch (eventType) {
    case 'click':
    case 'mousedown':
    case 'mouseup':
      event = new MouseEvent('click', {
        bubbles: true,
        cancelable: true,
        view: window,
      });
      break;
    case 'keypress':
    case 'keydown':
    case 'keyup':
      event = new KeyboardEvent(eventType, {
        bubbles: true,
        cancelable: true,
      });

      if (eventOption && eventOption.key) {
        event.key = eventOption.key;
      }
      break;
    default:
      event = new Event(eventType, {
        bubbles: true,
        cancelable: true,
      });

      if (eventOption && eventOption.key) {
        event.key = eventOption.key;
      }
  }

  return target.dispatchEvent(event);
}

export { simulateEvent };
