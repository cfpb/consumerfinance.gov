
'use strict';

// Required modules.
var EmailPopup = require( '../../organisms/EmailPopup' );
var EmailHelpers = require( '../../modules/util/email-popup-helpers' );

if ( $( '.o-email-popup' ).length ) {
  var popup = new EmailPopup( '.o-email-popup' );
  popup.init();
  EmailHelpers.showOnScroll( popup.el, {
  	cb: popup.showPopup,
    targetElement: $( '.tools-col .header-slug' )
  } );
}
