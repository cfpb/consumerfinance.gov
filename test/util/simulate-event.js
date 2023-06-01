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
    case 'mouseup': {
      event = new MouseEvent(eventType, {
        bubbles: true,
        cancelable: true,
        view: window,
      });
      break;
    }
    case 'keypress':
    case 'keydown':
    case 'keyup': {
      const opts = {
        bubbles: true,
        cancelable: true,
      };

      if (eventOption && eventOption.key) {
        opts.key = eventOption.key;
      }

      event = new KeyboardEvent(eventType, opts);

      break;
    }
    default: {
      event = new Event(eventType, {
        bubbles: true,
        cancelable: true,
      });
    }
  }

  return target.dispatchEvent(event);
}

export { simulateEvent };
