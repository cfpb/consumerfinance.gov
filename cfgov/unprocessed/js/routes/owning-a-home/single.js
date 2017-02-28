
'use strict';

// Required modules.
var EmailPopup = require( '../../organisms/EmailPopup' );
var emailHelpers = require( '../../modules/util/email-popup-helpers' );
if ( $( '.o-email-popup' ).length && emailHelpers.showEmailPopup() ) {
  var popup = new EmailPopup( '.o-email-popup' );
  popup.init();
  emailHelpers.showOnScroll( popup.el, {
  	cb: popup.showPopup,
  	targetElement: $('.o-info-unit-group')
  } );
}
