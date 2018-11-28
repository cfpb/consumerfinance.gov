import Notification from '../../../../cfgov/unprocessed/js/molecules/Notification';
const BASE_CLASS = 'm-notification';
const HTML_SNIPPET = `
  <div class="m-notification
              m-notification__default">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" class="cf-icon-svg"></svg>
    <div class="m-notification_content">
      <div class="h4 m-notification_message">Notification content</div>
    </div>
  </div>
`;

describe( 'Notification', () => {
  let notificationElem;
  let notification;
  let thisNotification;

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    notificationElem = document.querySelector( `.${ BASE_CLASS }` );
    notification = new Notification( notificationElem, BASE_CLASS, {} );
  } );

  describe( 'init()', () => {
    it( 'should return the Notification instance when initialized', () => {
      thisNotification = notification.init();
      expect( typeof thisNotification ).toStrictEqual( 'object' );
      expect( notificationElem.dataset.jsHook ).toStrictEqual( 'state_atomic_init' );
    } );

    it( 'should return undefined if already initialized', () => {
      notification.init();

      expect( notification.init() ).toBeUndefined();
    } );

    it( 'should return the Notification istance if it has a success class', () => {
      notificationElem.classList.remove( 'm-notification__default' );
      notificationElem.classList.add( 'm-notification__success' );

      notification.init();

      expect( notificationElem.dataset.jsHook ).toStrictEqual( 'state_atomic_init' );
    } );

    it( 'should return the Notification istance if it has a warning class', () => {
      notificationElem.classList.remove( 'm-notification__default' );
      notificationElem.classList.add( 'm-notification__warning' );

      notification.init();

      expect( notificationElem.dataset.jsHook ).toStrictEqual( 'state_atomic_init' );
    } );

    it( 'should return the Notification istance if it has a error class', () => {
      notificationElem.classList.remove( 'm-notification__default' );
      notificationElem.classList.add( 'm-notification__error' );

      notification.init();

      expect( notificationElem.dataset.jsHook ).toStrictEqual( 'state_atomic_init' );
    } );
  } );

  describe( 'setTypeAndContent()', () => {
    it( 'should update the notification type for the success state', () => {
      notification.init();

      notification.setTypeAndContent(
        notification.SUCCESS,
        ''
      );

      expect( notificationElem.classList ).toContain( 'm-notification__success' );
    } );

    it( 'should update the notification type for the warning state', () => {
      notification.init();

      notification.setTypeAndContent(
        notification.WARNING,
        ''
      );

      expect( notificationElem.classList ).toContain( 'm-notification__warning' );
    } );

    it( 'should update the notification type for the error state', () => {
      notification.init();

      notification.setTypeAndContent(
        notification.ERROR,
        ''
      );

      expect( notificationElem.classList ).toContain( 'm-notification__error' );
    } );

    it( 'should update the the notification message', () => {
      notification.init();

      notification.setTypeAndContent(
        notification.SUCCESS,
        'Notification message content'
      );

      const message = notificationElem.querySelector( '.m-notification_message' );
      const explanation = notificationElem.querySelector( '.m-notification_explanation' );

      expect( notificationElem.classList ).toContain( 'm-notification__success' );
      expect( message.textContent ).toContain( 'Notification message content' );
      expect( explanation ).toBeUndefined;
    } );

    it( 'should update the the notification explanation', () => {
      notification.init();

      notification.setTypeAndContent(
        notification.SUCCESS,
        'Notification message content',
        'Notification explanation content'
      );

      const message = notificationElem.querySelector( '.m-notification_message' );
      const explanation = notificationElem.querySelector( '.m-notification_explanation' );

      expect( notificationElem.classList ).toContain( 'm-notification__success' );
      expect( message.textContent ).toContain( 'Notification message content' );
      expect( explanation.textContent ).toContain( 'Notification explanation content' );
    } );
  } );
} );
