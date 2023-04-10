import { showOnScroll, showEmailPopup } from './email-popup-helpers.js';
import EmailPopup from '../../organisms/EmailPopup.js';

export default {
  init() {
    const emailPopup = document.querySelector('.' + EmailPopup.BASE_CLASS);

    if (emailPopup && showEmailPopup()) {
      const popup = new EmailPopup(emailPopup);
      popup.init();
      showOnScroll(popup.getDom(), {
        cb: popup.showPopup,
        targetElement: document.querySelector('.o-info-unit-group'),
      });
    }
  },
};
