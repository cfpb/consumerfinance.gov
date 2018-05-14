const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const Notification = require( BASE_JS_PATH + 'molecules/Notification' );
const BASE_CLASS = 'm-notification';
const HTML_SNIPPET = `
  <div class="m-notification
              m-notification__success
              m-notification__visible">
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
    thisNotification = notification.init();
  } );

  describe( 'init()', () => {
    it( 'should return the FormSubmit instance when initialized', () => {
      expect( typeof thisNotification ).toEqual( 'object' );
      expect( notificationElem.dataset.jsHook ).toEqual( 'state_atomic_init' );
    } );

    it( 'should return undefined if already initialized', () => {
      expect( notification.init() ).toBeUndefined();
    } );
  } );
} );
