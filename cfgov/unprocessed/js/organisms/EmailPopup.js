import {
  showEmailPopup,
  recordEmailPopupView,
  recordEmailRegistration,
  recordEmailPopupClosure,
} from '../modules/util/email-popup-helpers.js';
import { email as validatorsEmail } from '../modules/util/validators.js';
import {
  checkDom,
  setInitFlag,
} from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import FormSubmit from './FormSubmit.js';

/**
 * EmailPopup
 *
 * @class
 * @classdesc Initializes the organism.
 * @param {HTMLElement} element - The HTML DOM element.
 * @returns {EmailPopup} An instance.
 */
function EmailPopup(element) {
  const VISIBLE_CLASS = 'o-email-popup__visible';

  const _dom = checkDom(element, EmailPopup.BASE_CLASS);
  const _popupLabel = _dom.getAttribute('data-popup-label');

  // Set language default.
  let _language = 'en';

  /**
   * @returns {HTMLElement} The base element of the email popup.
   */
  function getDom() {
    return _dom;
  }

  /**
   * Function used to hide popup by removing visible class.
   *
   * @returns {EmailPopup} An instance.
   */
  function hidePopup() {
    _dom.classList.remove(VISIBLE_CLASS);
    recordEmailPopupClosure(_popupLabel);

    return this;
  }

  /**
   * Function used to show popup by adding visible class.
   *
   * @returns {boolean} True if the popup is shown, false otherwise.
   */
  function showPopup() {
    if (showEmailPopup(_popupLabel)) {
      _dom.classList.add(VISIBLE_CLASS);
      recordEmailPopupView(_popupLabel);
      return true;
    }

    return false;
  }

  /**
   * Function used to validate email address.
   *
   * @param {object} fields - An object containing form fields.
   * @returns {object} Validation status.
   */
  function emailValidation(fields) {
    return validatorsEmail(fields.email, '', { language: _language }).msg;
  }

  /**
   * Callback function invoked after successful email submission.
   */
  function _onEmailSignupSuccess() {
    recordEmailRegistration(_popupLabel);
  }

  /**
   * Function used to instatiate and initialize components.
   *
   * @returns {EmailPopup} An instance.
   */
  function init() {
    if (!setInitFlag(_dom)) {
      return this;
    }

    // Ensure EmailPopup is definitely hidden on initialization.
    _dom.classList.remove(VISIBLE_CLASS);

    const _closeElement = _dom.querySelector('.close');
    _language = _dom.getAttribute('lang');

    const formSubmit = new FormSubmit(_dom, EmailPopup.BASE_CLASS, {
      validator: emailValidation,
      language: _language,
    });

    formSubmit.init();

    formSubmit.addEventListener('success', _onEmailSignupSuccess);

    _closeElement.addEventListener('click', hidePopup);

    return this;
  }

  this.init = init;
  this.hidePopup = hidePopup;
  this.showPopup = showPopup;
  this.getDom = getDom;
  return this;
}
EmailPopup.BASE_CLASS = 'o-email-popup';

export default EmailPopup;
