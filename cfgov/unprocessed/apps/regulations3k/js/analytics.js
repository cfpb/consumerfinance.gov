import Analytics from '../../../js/modules/Analytics';
import { queryOne as find } from '../../../js/modules/util/dom-traverse';

/**
 * Sends the user interaction to Analytics
 * @param {string} action - The user's action
 * @param {string} label - The label associated with the action
 * @param {string} category - Optional category if it's not eRegs-related
 * @returns {object} Event data
 */
const sendEvent = ( action, label, category ) => {
  category = category || 'eRegs Event';
  const eventData = Analytics.getDataLayerOptions( action, label, category );
  Analytics.sendEvent( eventData );
  return eventData;
};

module.exports = {
  sendEvent
};
