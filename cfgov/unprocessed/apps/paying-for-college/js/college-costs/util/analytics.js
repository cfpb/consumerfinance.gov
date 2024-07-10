import { analyticsSendEvent } from '@cfpb/cfpb-analytics';

/**
 * Sends an event to the dataLayer for Google Tag Manager
 * @param {string|object} action - The type of event or action taken, OR a payload Object
 * @param {string} label - A value or label for the action
 */
function sendAnalyticsEvent(action, label) {
  if ( typeof action === 'object' ) {
    analyticsSendEvent(payload);
    return payload;
  } else {
    analyticsSendEvent({
      action,
      label,
      event: 'P4C Financial Path Interaction',
    });    
  }

}

export { sendAnalyticsEvent };
