import { analyticsSendEvent } from '@cfpb/cfpb-analytics';

/**
 * Sends the user interaction to Analytics
 * @param {string} action - The user's action
 * @param {string} label - The label associated with the action
 * @param {string} category - Optional category if it's not eRegs-related
 * @returns {object} Event data
 */
const sendEvent = (action, label, category) => {
  const event = category || 'eRegs Event';
  const payload = { action, label, event };
  analyticsSendEvent(payload);
  return payload;
};

/**
 * getExpandable - Find the expandable the user clicked.
 * @param {event} event - Click event.
 * @returns {HTMLElement|null} The expandable or null if it's not an expandable
 */
const getExpandable = (event) => {
  const el = event.target.closest('.o-expandable__header') || event.target;
  if (el.classList.contains('o-expandable__header')) {
    return el;
  }
  return null;
};

/**
 * getExpandableState - TODO add description
 * @param {HTMLElement} expandable - Expandable's HTML element.
 * @returns {string} Expandable's state, either `open` or `close`.
 */
const getExpandableState = (expandable) => {
  let state = 'close';
  if (expandable.classList.contains('o-expandable__target--expanded')) {
    state = 'open';
  }
  return state;
};

/**
 * handleNavClick - Listen for secondary nav clicks and report to GA if it's a
 * link to a reg section.
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleNavClick = (event) => {
  if (!event.target.href) {
    return;
  }
  // Double check that the URL ends in regulations/1234/XXXXXX
  let section = event.target.href.match(/regulations\/(\d+\/[\w-]+)\/?$/);
  if (!section) {
    return;
  }
  section = section[1].replace('/', '-');
  return sendEvent('toc:click', section);
};

/**
 * handleContentClick - Listen for clicks within a reg section's content
 * and report to GA if they opened or closed an expandable.
 * @param {event} event - Click event.
 * @returns {object} Event data.
 */
const handleContentClick = (event) => {
  const expandable = getExpandable(event);
  if (!expandable) {
    return;
  }
  const action = `interpexpandables:${getExpandableState(expandable)}`;
  const section = expandable.getAttribute('data-section');
  return sendEvent(action, section);
};

export {
  getExpandable,
  getExpandableState,
  handleContentClick,
  handleNavClick,
  sendEvent,
};
