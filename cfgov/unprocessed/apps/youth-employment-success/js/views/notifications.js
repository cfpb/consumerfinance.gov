import { toggleCFNotification } from '../util';
import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import { getBitmask } from '../data-types/notifications';
import buildAlertRules from '../details-notification-rules';

const CLASSES = Object.freeze( {
  CONTAINER: 'js-route-notifications',
  INVALID_ALERT: 'js-route-invalid',
  INCOMPLETE_ALERT: 'js-route-incomplete',
  PENDING_TODOS_ALERT: 'js-route-pending-todos',
  OOB_ALERT: 'js-route-oob',
  OOB_W_TODOS: 'js-route-oob-with-todos',
  IN_BUDGET_ALERT: 'js-route-complete',
  IN_BUDGET_W_TODOS: 'js-route-complete-with-todos'
} );

const alertRules = buildAlertRules( CLASSES );

/**
 * NotificationsView
 * @class
 *
 * @classdesc View to handle showing and hiding of various notifications
 *
 * @param {HTMLNode} element The root DOM element for this view
 * @returns {Object} This view's public methods
 */
function notificationsView( element ) {
  const _dom = checkDom( element, CLASSES.CONTAINER );
  let activeNotification;

  /**
   * Remove active alert notification from the DOM, and zero out the reference to it.
   * @param {HTMLElement} alertContainer The DOM element from which the alert should be removed
   */
  function _clearActiveNotification( alertContainer ) {
    toggleCFNotification( activeNotification, false );
    alertContainer.removeChild( activeNotification );
    alertContainer.classList.add( 'u-hidden' );
    activeNotification = null;
  }

  /**
   * Toggle the supplied notification, as well as the notifications container element, if necessary.
   * @param {HTMLElement} alertEl The DOM node of the notification to toggle
   * @param {HTMLElement} alertContainer The DOM node in which to render the notification
   * @param {Boolean} doShow Whether to show or hide the notification
   */
  function _updateNotificationVisibility( alertEl, alertContainer, doShow ) {
    if ( activeNotification ) {
      _clearActiveNotification( alertContainer );
    }

    if ( alertEl ) {
      activeNotification = alertEl.cloneNode( true );
      toggleCFNotification( activeNotification, doShow );
      alertContainer.appendChild( activeNotification );
      alertContainer.classList.remove( 'u-hidden' );
      _dom.classList.remove( 'u-hidden' );
    } else {
      _dom.classList.add( 'u-hidden' );
    }
  }

  return {
    init() {
      if ( setInitFlag( _dom ) ) {
        _dom.classList.add( 'u-hidden' );
      }

      return this;
    },
    render( { alertValues, alertTarget } ) {
      const alertSelector = alertRules[getBitmask( alertValues )];
      const alertEl = _dom.querySelector( `.${ alertSelector }` );

      _updateNotificationVisibility( alertEl, alertTarget, true );
    }
  };
}

notificationsView.CLASSES = CLASSES;

export default notificationsView;
