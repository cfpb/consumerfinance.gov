import { analyticsSendEvent } from '@cfpb/cfpb-analytics';

/**
 * Sends an event to the dataLayer for Google Tag Manager
 * @param {string} action - The type of event or action taken
 * @param {string} label - A value or label for the action
 */
function sendAnalyticsEvent(action, label) {
  analyticsSendEvent({
    action,
    label,
    event: 'P4C Financial Path Interaction',
  });
}

export { sendAnalyticsEvent };
