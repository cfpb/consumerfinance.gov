import {
  notificationsView
} from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/notifications';
import {
  ALERT_TYPES
} from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/data-types/notifications';

const CLASSES = notificationsView.CLASSES;
const NOTIFICATION_CLASS = 'm-notification';
const VISIBLE_NOTIFICATION_CLASS = 'm-notification__visible';

const HTML = `
  <div class="${ CLASSES.CONTAINER }">  
    <div class="${ CLASSES.INVALID_ALERT }">
      <div class="m-notification">
        <div class="m-notification_content"></div>
      </div>
    </div>
    <div class="${ CLASSES.INCOMPLETE_ALERT }">
      <div class="m-notification">
        <div class="m-notification_content"></div>
      </div> 
    </div>
    <div class="${ CLASSES.OOB_ALERT }">
      <div class="m-notification">
        <div class="m-notification_content"></div>
      </div>
    </div>
    <div class="${ CLASSES.OOB_W_TODOS }">
      <div class="m-notification">
        <div class="m-notification_content"></div>
      </div>
    </div>
    <div class="${ CLASSES.IN_BUDGET_ALERT }">
      <div class="m-notification">
        <div class="m-notification_content"></div>
      </div>
    </div>
    <div class="${ CLASSES.IN_BUDGET_W_TODOS }">
      <div class="m-notification">
        <div class="m-notification_content"></div>
      </div>
    </div>
  </div>
  <div class="target"></div>
`;

const alertSettings = {
  [ALERT_TYPES.HAS_TODOS]: false,
  [ALERT_TYPES.INVALID]: false,
  [ALERT_TYPES.IN_BUDGET]: false,
  [ALERT_TYPES.OUT_OF_BUDGET]: false
};

describe( 'notificationsView', () => {
  let dom;
  let alertTarget;
  let view;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    dom = document.body.querySelector( `.${ CLASSES.CONTAINER }` );
    alertTarget = document.body.querySelector( '.target' );
    view = notificationsView( dom );
    view.init();
  } );

  afterEach( () => {
    document.body.innerHTML = null;
    view = null;
  } );

  it( 'initializes with the notifications container hidden', () => {
    expect( dom.classList.contains( 'u-hidden' ) ).toBeTruthy();
  } );

  it( 'toggles its container element when ' +
      'there is an active notification', () => {
    view.render( {
      alertValues: {
        ...alertSettings,
        [ALERT_TYPES.INVALID]: true
      },
      alertTarget } );

    expect( dom.classList.contains( 'u-hidden' ) ).toBeFalsy();
  } );

  describe( 'alert visibility', () => {
    it( 'clears an active alert when a new one is supplied', () => {
      view.render( {
        alertValues: {
          ...alertSettings,
          [ALERT_TYPES.INVALID]: true
        },
        alertTarget } );

      let alert = alertTarget.querySelector( `.${ CLASSES.INVALID_ALERT }` );

      expect( alert ).toBeDefined();

      view.render( {
        alertValues: {
          ...alertSettings,
          [ALERT_TYPES.INVALID]: false,
          [ALERT_TYPES.IN_BUDGET]: true
        },
        alertTarget } );

      alert = alertTarget.querySelector( `.${ CLASSES.INVALID_ALERT }` );

      expect( alert === null ).toBeTruthy();

      alert = alertTarget.querySelector( `.${ CLASSES.IN_BUDGET_ALERT }` );
      expect( alert ).toBeDefined();
    } );

    it( 'displays the invalid alert when data is invalid', () => {
      view.render( {
        alertValues: {
          ...alertSettings,
          [ALERT_TYPES.INVALID]: true
        },
        alertTarget } );

      const alert = alertTarget.querySelector(
        `.${ CLASSES.INVALID_ALERT }`
      );
      const alertNotification = alert.querySelector(
        `.${ NOTIFICATION_CLASS }`
      );

      expect( alertNotification.classList.contains(
        `${ VISIBLE_NOTIFICATION_CLASS }`
      ) ).toBeTruthy();
      expect( alertTarget.childNodes.length ).toBe( 1 );
    } );

    it( 'displays the invalid with todos alert when ' +
        'data is invalid and there are todos', () => {
      view.render( {
        alertValues: {
          ...alertSettings,
          [ALERT_TYPES.INVALID]: true,
          [ALERT_TYPES.HAS_TODOS]: true
        },
        alertTarget } );

      const alert = alertTarget.querySelector(
        `.${ CLASSES.INCOMPLETE_ALERT }`
      );
      const alertNotification = alert.querySelector(
        `.${ NOTIFICATION_CLASS }`
      );

      expect( alertNotification.classList.contains(
        `${ VISIBLE_NOTIFICATION_CLASS }`
      ) ).toBeTruthy();
      expect( alertTarget.childNodes.length ).toBe( 1 );
    } );

    it( 'displays the in budget alert when data is in budget', () => {
      view.render( {
        alertValues: {
          ...alertSettings,
          [ALERT_TYPES.IN_BUDGET]: true
        },
        alertTarget } );

      const alert = alertTarget.querySelector(
        `.${ CLASSES.IN_BUDGET_ALERT }`
      );
      const alertNotification = alert.querySelector(
        `.${ NOTIFICATION_CLASS }`
      );

      expect( alertNotification.classList.contains(
        `${ VISIBLE_NOTIFICATION_CLASS }`
      ) ).toBeTruthy();
      expect( alertTarget.childNodes.length ).toBe( 1 );
    } );

    it( 'displays the in-budget-with-todos alert when ' +
        'data is in budget and there are todos', () => {
      view.render( {
        alertValues: {
          ...alertSettings,
          [ALERT_TYPES.IN_BUDGET]: true,
          [ALERT_TYPES.HAS_TODOS]: true
        },
        alertTarget } );

      const alert = alertTarget.querySelector(
        `.${ CLASSES.IN_BUDGET_W_TODOS }`
      );
      const alertNotification = alert.querySelector(
        `.${ NOTIFICATION_CLASS }`
      );

      expect( alertNotification.classList.contains(
        `${ VISIBLE_NOTIFICATION_CLASS }`
      ) ).toBeTruthy();
      expect( alertTarget.childNodes.length ).toBe( 1 );
    } );

    it( 'displays out of budget alert when data is out of budget', () => {
      view.render( {
        alertValues: {
          ...alertSettings,
          [ALERT_TYPES.OUT_OF_BUDGET]: true
        },
        alertTarget } );

      const alert = alertTarget.querySelector(
        `.${ CLASSES.OOB_ALERT }`
      );
      const alertNotification = alert.querySelector(
        `.${ NOTIFICATION_CLASS }`
      );

      expect( alertNotification.classList.contains(
        `${ VISIBLE_NOTIFICATION_CLASS }`
      ) ).toBeTruthy();
      expect( alertTarget.childNodes.length ).toBe( 1 );
    } );

    it( 'displays out-of-budget-with-todos alert when ' +
        'data is out of budget and there are todos', () => {
      view.render( {
        alertValues: {
          ...alertSettings,
          [ALERT_TYPES.OUT_OF_BUDGET]: true,
          [ALERT_TYPES.HAS_TODOS]: true
        },
        alertTarget } );

      const alert = alertTarget.querySelector(
        `.${ CLASSES.OOB_W_TODOS }`
      );
      const alertNotification = alert.querySelector(
        `.${ NOTIFICATION_CLASS }`
      );

      expect( alertNotification.classList.contains(
        `${ VISIBLE_NOTIFICATION_CLASS }`
      ) ).toBeTruthy();
      expect( alertTarget.childNodes.length ).toBe( 1 );
    } );

    it( 'does not display anything when invalid bitmask is supplied', () => {
      view.render( {
        alertValues: {
          ...alertSettings,
          [ALERT_TYPES.OUT_OF_BUDGET]: true,
          [ALERT_TYPES.IN_BUDGET]: true
        },
        alertTarget } );

      expect( alertTarget.childNodes.length ).toBe( 0 );
    } );
  } );
} );
