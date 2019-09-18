import Notification from '../../../../cfgov/unprocessed/js/molecules/Notification';

const HTML_SNIPPET = `
<div class="m-notification">
  <svg xmlns="http://www.w3.org/2000/svg"
       viewBox="0 0 1000 1200" class="cf-icon-svg"></svg>
  <div class="m-notification_content">
    <div class="h4 m-notification_message">Notification content</div>
  </div>
</div>
`;

describe( 'Notification', () => {
  const notificationSel = '.m-notification';
  let notificationElem;
  let notification;

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    notificationElem = document.querySelector( notificationSel );
    notification = new Notification( notificationElem );
  } );

  describe( 'init()', () => {
    it( 'should return the instance when initialized', () => {
      expect( notification.init() ).toBeInstanceOf( Notification );
      expect( notificationElem.dataset.jsHook ).toBe( 'state_atomic_init' );
      expect( notification.init() ).toBeInstanceOf( Notification );
    } );

    it( 'should return the Notification instance if it has a success class',
      () => {
        notificationElem.classList.add( 'm-notification__success' );

        expect( notification.init().constructor ).toBe( Notification );
        expect( notificationElem.dataset.jsHook ).toBe( 'state_atomic_init' );
      }
    );

    it( 'should return the Notification instance if it has a warning class',
      () => {
        notificationElem.classList.add( 'm-notification__warning' );

        expect( notification.init().constructor ).toBe( Notification );
        expect( notificationElem.dataset.jsHook ).toBe( 'state_atomic_init' );
      }
    );

    it( 'should return the Notification instance if it has a error class',
      () => {
        notificationElem.classList.add( 'm-notification__error' );

        expect( notification.init().constructor ).toBe( Notification );
        expect( notificationElem.dataset.jsHook ).toBe( 'state_atomic_init' );
      }
    );
  } );

  describe( 'update()', () => {

    beforeEach( () => {
      notification.init();
    } );

    it( 'should throw an error for unsupported type', () => {
      try {
        // TODO: The Notification should probably support setting the default.
        notification.update( 'default', '' );
      } catch ( error ) {
        expect( error.message )
          .toBe( 'default is not a supported notification type!' );
      }
    } );

    it( 'should update the notification type for the success state', () => {
      notification.update( Notification.SUCCESS, '' );
      expect( notificationElem.className )
        .toContain( 'm-notification__success' );
    } );

    it( 'should update the notification type for the warning state', () => {
      notification.update( Notification.WARNING, '' );
      expect( notificationElem.className )
        .toContain( 'm-notification__warning' );
    } );

    it( 'should update the notification type for the error state', () => {
      notification.update( Notification.ERROR, '' );
      expect( notificationElem.className ).toContain( 'm-notification__error' );
    } );

    it( 'should update the the notification message', () => {
      const testMsg = 'Notification message content';
      notification.update( Notification.SUCCESS, testMsg );

      const message = notificationElem.querySelector(
        '.m-notification_message'
      );
      const explanation = notificationElem.querySelector(
        '.m-notification_explanation'
      );

      expect( notificationElem.className )
        .toContain( 'm-notification__success' );
      expect( message.textContent ).toContain( testMsg );
      expect( explanation ).toBeUndefined;
    } );

    it( 'should update the notification explanation', () => {
      const testMsg = 'Notification message content';
      const testExplanation = 'Notification explanation content';
      notification.update( Notification.SUCCESS, testMsg, testExplanation );

      const message = notificationElem.querySelector(
        '.m-notification_message'
      );
      const explanation = notificationElem.querySelector(
        '.m-notification_explanation'
      );

      expect( notificationElem.className )
        .toContain( 'm-notification__success' );
      expect( message.textContent ).toContain( testMsg );
      expect( explanation.textContent ).toContain( testExplanation );
    } );
  } );
} );
