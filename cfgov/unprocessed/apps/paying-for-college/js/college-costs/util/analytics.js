import { analyticsSendEvent } from '@cfpb/cfpb-analytics';

/**
 * Sends an event to the dataLayer for Google Tag Manager
 * @param {string|object} action - The type of event or action taken, OR a payload Object
 * @param {string} label - A value or label for the action
 */
function sendAnalyticsEvent(action, label) {
  // Handle payload-style events
  if (typeof action === 'object') {
    analyticsSendEvent(action);
    return action;
  } else {
    analyticsSendEvent({
      action,
      label,
      event: 'P4C Financial Path Interaction',
    });
  }
}

/**
 * A simple function to track tooltip engagement
 */
function toolTipTracking() {
  const tooltips = document.querySelectorAll('.a-tooltip');
  tooltips.forEach((elem) => {
    const parentText = elem.parentElement.innerText;
    elem.addEventListener('mouseenter', () => {
      sendAnalyticsEvent('Tooltip Mouseenter', parentText);
    });
  });
}

export { sendAnalyticsEvent, toolTipTracking };
