import Analytics from '../../../../js/modules/Analytics';

/**
 * Sends an event to the dataLayer for Google Tag Manager
 * @param {string} action - The type of event or action taken
 * @param {string} label - A value or label for the action
 */
function sendAnalyticsEvent( action, label ) {
  const eventData = Analytics.getDataLayerOptions( action, label, 'P4C Financial Path Interaction' );
  Analytics.sendEvent( eventData );
}

export {
  sendAnalyticsEvent
};
