import Analytics from '../../../js/modules/Analytics';
import { closest } from '@cfpb/cfpb-atomic-component/src/utilities/dom-traverse.js';

/* eslint-disable consistent-return */

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

/**
 * getExpandable - Find the expandable the user clicked.
 *
 * @param {event} event Click event
 *
 * @returns {DOMNode|null} The expandable or null if it's not an expandable
 */
const getExpandable = event => {
  const el = closest( event.target, '.o-expandable_header' ) || event.target;
  if ( el.classList.contains( 'o-expandable_header' ) ) {
    return el;
  }
  return null;
};


/**
 * getExpandableState - Description
 *
 * @param {DOMNode} expandable Expandable's HTML element
 *
 * @returns {string} Expandable's state, either `open` or `close`
 */
const getExpandableState = expandable => {
  let state = 'close';
  if ( expandable.classList.contains( 'o-expandable_target__expanded' ) ) {
    state = 'open';
  }
  return state;
};

/**
 * handleNavClick - Listen for secondary nav clicks and report to GA if it's a
 * link to a reg section.
 *
 * @param {event} event Click event
 * @returns {object} Event data
 */
const handleNavClick = event => {
  if ( !event.target.href ) {
    return;
  }
  // Double check that the URL ends in regulations/1234/XXXXXX
  let section = event.target.href.match( /regulations\/(\d+\/[\w-]+)\/?$/ );
  if ( !section ) {
    return;
  }
  section = section[1].replace( '/', '-' );
  return sendEvent( 'toc:click', section );
};

/**
 * handleContentClick - Listen for clicks within a reg section's content
 * and report to GA if they opened or closed an expandable.
 *
 * @param {event} event Click event
 * @returns {object} Event data
 */
const handleContentClick = event => {
  const expandable = getExpandable( event );
  if ( !expandable ) {
    return;
  }
  const action = `interpexpandables:${ getExpandableState( expandable ) }`;
  const section = expandable.getAttribute( 'data-section' );
  return sendEvent( action, section );
};

export {
  getExpandable,
  getExpandableState,
  handleContentClick,
  handleNavClick,
  sendEvent
};
