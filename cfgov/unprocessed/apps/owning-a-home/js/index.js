const EmailPopup = require( '../../../js/organisms/EmailPopup' );
const emailHelpers = require( '../../../js/modules/util/email-popup-helpers' );
const emailPopup = document.querySelectorAll( '.o-email-popup' );

if ( emailPopup.length && emailHelpers.showEmailPopup() ) {
  const popup = new EmailPopup();
  popup.init();
  emailHelpers.showOnScroll( popup.el, {
    cb: popup.showPopup,
    targetElement: document.querySelector( '.o-info-unit-group' )
  } );
}
