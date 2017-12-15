const EmailPopup = require( '../../../organisms/EmailPopup' );
const emailHelpers = require( '../../../modules/util/email-popup-helpers' );
const emailPopup = document.querySelectorAll( '.o-email-popup' );

if ( emailPopup.length && emailHelpers.showEmailPopup() ) {
  const popup = new EmailPopup( '.o-email-popup' );
  popup.init();
  emailHelpers.showOnScroll( popup.el, {
    cb: popup.showPopup,
    targetElement: document.querySelector( '.o-info-unit-group' )
  } );
}
