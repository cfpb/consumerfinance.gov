const Notification = require( '../../molecules/Notification' );
const EmailPopup = require( '../../organisms/EmailPopup' );
const emailHelpers = require( './email-popup-helpers' );
const emailPopup = document.querySelector( '.' + EmailPopup.BASE_CLASS );

if ( emailPopup && emailHelpers.showEmailPopup() ) {
  const _notification = new Notification( emailPopup );
  _notification.init();

  const popup = new EmailPopup( emailPopup, _notification );
  popup.init();

  emailHelpers.showOnScroll( popup.getDom(), {
    cb: popup.showPopup,
    targetElement: document.querySelector( '.o-info-unit-group' )
  } );
}
