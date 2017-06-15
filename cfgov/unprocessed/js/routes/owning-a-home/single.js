
'use strict';

// Required modules.
var EmailPopup = require( '../../organisms/EmailPopup' );
var emailHelpers = require( '../../modules/util/email-popup-helpers' );
var emailPopup = document.querySelectorAll( '.o-email-popup' )


if ( emailPopup && emailHelpers.showEmailPopup() ) {

  var popup = new EmailPopup( '.o-email-popup' );
  popup.init();
  emailHelpers.showOnScroll( popup.el, {
  	cb: popup.showPopup,
  	targetElement: document.querySelector( '.o-info-unit-group' )
  } );
}
