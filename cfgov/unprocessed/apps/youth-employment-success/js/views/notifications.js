import { toggleCFNotification } from '../util';
import { checkDom, setInitFlag } from '../../../../js/modules/util/atomic-helpers';
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
   * Toggle the supplied notification, as well as the notifications container element, if necessary.
   * @param {HTMLElement} notificationEl The DOM node of the notification to toggle
   * @param {Boolean} doShow Whether to show or hide the notification
   */
  function _updateNotificationVisibility( notificationEl, doShow ) {
    if ( activeNotification ) {
      toggleCFNotification( activeNotification, false );
      activeNotification = null;
    }

    activeNotification = notificationEl;
    toggleCFNotification( activeNotification, doShow );

    if ( activeNotification ) {
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
    render( alertValues ) {
      const alertEl = alertRules[getBitmask( alertValues )];
      _updateNotificationVisibility( _dom.querySelector( `.${ alertEl }` ), true );
    }
  };
}

notificationsView.CLASSES = CLASSES;

export default notificationsView;
