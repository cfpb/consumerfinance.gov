const EmailPopup = require( '../../../../js/organisms/EmailPopup' );
const emailHelpers = require( '../../../../js/modules/util/email-popup-helpers' );
const emailPopup = document.querySelector( '.' + EmailPopup.BASE_CLASS );

if ( emailPopup && emailHelpers.showEmailPopup() ) {
  const popup = new EmailPopup( emailPopup );
  popup.init();
  emailHelpers.showOnScroll( popup.getDom(), {
    cb: popup.showPopup,
    targetElement: document.querySelector( '.o-info-unit-group' )
  } );
}
