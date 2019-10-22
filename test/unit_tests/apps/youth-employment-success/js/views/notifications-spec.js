import notificationsView from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/views/notifications';
import { toArray } from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/util';
import { ALERT_TYPES } from '../../../../../../cfgov/unprocessed/apps/youth-employment-success/js/data-types/notifications';

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
    <div class="${ CLASSES.PENDING_TODOS_ALERT }">
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
`;

const alertValues = {
  [ALERT_TYPES.HAS_TODOS]: false,
  [ALERT_TYPES.INVALID]: false,
  [ALERT_TYPES.IN_BUDGET]: false,
  [ALERT_TYPES.OUT_OF_BUDGET]: false
};

describe( 'notificationsView', () => {
  let dom;
  let alerts;
  let view;

  beforeEach( () => {
    document.body.innerHTML = HTML;
    dom = document.body.querySelector( `.${ CLASSES.CONTAINER }` );
    view = notificationsView( dom );
    view.init();
    alerts = toArray( dom.querySelectorAll( 'div[class^="js-route"]' ) );
  } );

  afterEach( () => {
    alerts.length = 0;
    document.body.innerHTML = null;
    view = null;
  } );

  it( 'initializes with the notifications container hidden', () => {
    expect( dom.classList.contains( 'u-hidden' ) ).toBeTruthy();
  } );

  it( 'toggles its container element when a there is an active notification', () => {
    view.render( {
      ...alertValues,
      [ALERT_TYPES.HAS_TODOS]: true
    } );

    expect( dom.classList.contains( 'u-hidden' ) ).toBeFalsy();
  } );

  it( 'hides the previous alert and shows a new one when values change', () => {
    view.render( {
      ...alertValues,
      [ALERT_TYPES.HAS_TODOS]: true
    } );

    let alertIndex = alerts.findIndex( el => el.classList.contains( `${ CLASSES.PENDING_TODOS_ALERT }` ) );
    let alertNotification = alerts[alertIndex].querySelector( `.${ NOTIFICATION_CLASS }` );

    expect( alertNotification.classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` ) ).toBeTruthy();

    view.render( {
      ...alertValues,
      [ALERT_TYPES.INVALID]: true
    } );

    expect( alertNotification.classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` ) ).toBeFalsy();

    alertIndex = alerts.findIndex( el => el.classList.contains( `${ CLASSES.INVALID_ALERT }` ) );
    alertNotification = alerts[alertIndex].querySelector( `.${ NOTIFICATION_CLASS }` );

    expect( alertNotification.classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` ) ).toBeTruthy();
  } );

  describe( 'alert visibility', () => {
    it( 'displays the invalid alert when data is invalid', () => {
      view.render( {
        ...alertValues,
        [ALERT_TYPES.INVALID]: true
      } );

      const invalidAlertIndex = alerts.findIndex( el => el.classList.contains( `${ CLASSES.INVALID_ALERT }` ) );

      const alert = alerts.splice( invalidAlertIndex, 1 );
      const alertNotification = alert[0].querySelector( `.${ NOTIFICATION_CLASS }` );

      expect( alertNotification.classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` ) ).toBeTruthy();

      alerts.forEach( alert => {
        expect(
          alert.querySelector( `.${ NOTIFICATION_CLASS }` ).classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` )
        ).toBeFalsy();
      } );
    } );

    it( 'displays the invalid with todos alert when data is invalid and there are todos', () => {
      view.render( {
        ...alertValues,
        [ALERT_TYPES.INVALID]: true,
        [ALERT_TYPES.HAS_TODOS]: true
      } );

      const alertIndex = alerts.findIndex( el => el.classList.contains( `${ CLASSES.INCOMPLETE_ALERT }` )
      );
      const alert = alerts.splice( alertIndex, 1 );
      const alertNotification = alert[0].querySelector( `.${ NOTIFICATION_CLASS }` );

      expect( alertNotification.classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` ) ).toBeTruthy();

      alerts.forEach( alert => {
        expect(
          alert.querySelector( `.${ NOTIFICATION_CLASS }` ).classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` )
        ).toBeFalsy();
      } );
    } );

    it( 'displays the pending todos alert when data is valid and there are todos', () => {
      view.render( {
        ...alertValues,
        [ALERT_TYPES.HAS_TODOS]: true
      } );

      const alertIndex = alerts.findIndex( el => el.classList.contains( `${ CLASSES.PENDING_TODOS_ALERT }` )
      );
      const alert = alerts.splice( alertIndex, 1 );
      const alertNotification = alert[0].querySelector( `.${ NOTIFICATION_CLASS }` );

      expect( alertNotification.classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` ) ).toBeTruthy();

      alerts.forEach( alert => {
        expect(
          alert.querySelector( `.${ NOTIFICATION_CLASS }` ).classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` )
        ).toBeFalsy();
      } );
    } );

    it( 'displays the in budget alert when data is in budget', () => {
      view.render( {
        ...alertValues,
        [ALERT_TYPES.IN_BUDGET]: true
      } );

      const alertIndex = alerts.findIndex( el => el.classList.contains( `${ CLASSES.IN_BUDGET_ALERT }` )
      );
      const alert = alerts.splice( alertIndex, 1 );
      const alertNotification = alert[0].querySelector( `.${ NOTIFICATION_CLASS }` );

      expect( alertNotification.classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` ) ).toBeTruthy();

      alerts.forEach( alert => {
        expect(
          alert.querySelector( `.${ NOTIFICATION_CLASS }` ).classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` )
        ).toBeFalsy();
      } );
    } );

    it( 'displays the in-budget-with-todos alert when data is in budget and there are todos', () => {
      expect( view.render( {
        ...alertValues,
        [ALERT_TYPES.IN_BUDGET]: true,
        [ALERT_TYPES.HAS_TODOS]: true
      } ) );

      const alertIndex = alerts.findIndex( el => el.classList.contains( `${ CLASSES.IN_BUDGET_W_TODOS }` )
      );
      const alert = alerts.splice( alertIndex, 1 );
      const alertNotification = alert[0].querySelector( `.${ NOTIFICATION_CLASS }` );

      expect( alertNotification.classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` ) ).toBeTruthy();

      alerts.forEach( alert => {
        expect(
          alert.querySelector( `.${ NOTIFICATION_CLASS }` ).classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` )
        ).toBeFalsy();
      } );
    } );

    it( 'displays the out of budget alert when data is out of budget', () => {
      view.render( {
        ...alertValues,
        [ALERT_TYPES.OUT_OF_BUDGET]: true
      } );

      const alertIndex = alerts.findIndex( el => el.classList.contains( `${ CLASSES.OOB_ALERT }` )
      );
      const alert = alerts.splice( alertIndex, 1 );
      const alertNotification = alert[0].querySelector( `.${ NOTIFICATION_CLASS }` );

      expect( alertNotification.classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` ) ).toBeTruthy();

      alerts.forEach( alert => {
        expect(
          alert.querySelector( `.${ NOTIFICATION_CLASS }` ).classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` )
        ).toBeFalsy();
      } );
    } );

    it( 'displays the out-of-budget-with-todos alert when data is out of budget and there are todos', () => {
      view.render( {
        ...alertValues,
        [ALERT_TYPES.OUT_OF_BUDGET]: true,
        [ALERT_TYPES.HAS_TODOS]: true
      } );

      const alertIndex = alerts.findIndex( el => el.classList.contains( `${ CLASSES.OOB_W_TODOS }` )
      );
      const alert = alerts.splice( alertIndex, 1 );
      const alertNotification = alert[0].querySelector( `.${ NOTIFICATION_CLASS }` );

      expect( alertNotification.classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` ) ).toBeTruthy();

      alerts.forEach( alert => {
        expect(
          alert.querySelector( `.${ NOTIFICATION_CLASS }` ).classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` )
        ).toBeFalsy();
      } );
    } );

    it( 'does not display anything when an invalid bitmask is supplied', () => {
      view.render( {
        ...alertValues,
        [ALERT_TYPES.OUT_OF_BUDGET]: true,
        [ALERT_TYPES.IN_BUDGET]: true
      } );

      alerts.forEach( alert => {
        expect(
          alert.querySelector( `.${ NOTIFICATION_CLASS }` ).classList.contains( `${ VISIBLE_NOTIFICATION_CLASS }` )
        ).toBeFalsy();
      } );
    } );
  } );
} );
