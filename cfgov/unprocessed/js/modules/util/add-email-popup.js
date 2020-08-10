import * as emailHelpers from './email-popup-helpers';
import EmailPopup from '../../organisms/EmailPopup';

const emailPopup = document.querySelector( '.' + EmailPopup.BASE_CLASS );

if ( emailPopup && emailHelpers.showEmailPopup() ) {
  const popup = new EmailPopup( emailPopup );
  popup.init();
  emailHelpers.showOnScroll( popup.getDom(), {
    cb: popup.showPopup,
    targetElement: document.querySelector( '.o-info-unit-group' )
  } );
}
