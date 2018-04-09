const FormSubmit = require( './FormSubmit.js' );
const atomicHelpers = require( '../modules/util/atomic-helpers' );
const standardType = require( '../modules/util/standard-type' );
const validators = require( '../modules/util/validators' );
const emailHelpers = require( '../modules/util/email-popup-helpers' );

/**
 * EmailPopup
 * @class
 *
 * @classdesc Initializes the organism.
 *
 * @param {string} element
 *   The selector for the organism.
 * @param {object} _notification Instance of Notification associated
 *   with this form.
 * @returns {EmailSignup} An instance.
 */
function EmailPopup( element, _notification ) {
  const VISIBLE_CLASS = 'o-email-popup__visible';
  const _dom = atomicHelpers.checkDom( element, EmailPopup.BASE_CLASS );
  const _popupLabel = _dom.getAttribute( 'data-popup-label' );

  // Set language default.
  let _language = 'en';

  /**
   * @returns {HTMLNode} The base element of the email popup.
   */
  function getDom() {
    return _dom;
  }

  /**
   * Function used to hide popup by removing visible class.
   * @returns {EmailPopup} An instance.
   */
  function hidePopup() {
    _dom.classList.remove( VISIBLE_CLASS );
    emailHelpers.recordEmailPopupClosure( _popupLabel );

    return this;
  }

  /**
   * Function used to show popup by adding visible class.
   * @returns {boolean} True if the popup is shown, false otherwise.
   */
  function showPopup() {
    if ( emailHelpers.showEmailPopup( _popupLabel ) ) {
      _dom.classList.add( VISIBLE_CLASS );
      emailHelpers.recordEmailPopupView( _popupLabel );
      return true;
    }

    return false;
  }

  /**
   * Function used to validate email address.
   * @param {Object} fields An object containing form fields.
   * @returns {Object} Validation status.
   */
  function emailValidation( fields ) {

    return validators.email(
      fields.email,
      '',
      { language: _language }
    ).msg;
  }

  /**
   * Callback function invoked after successful email submission.
   * @param {Event} event Click event.
   *
   */
  function _onEmailSignupSuccess() {
    emailHelpers.recordEmailRegistration( _popupLabel );
  }

  /**
   * Function used to instatiate and initialize components.
   * @returns {EmailPopup|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }

    // Ensure EmailPopup is definitely hidden on initialization.
    _dom.classList.remove( VISIBLE_CLASS );

    const _closeElement = _dom.querySelector( '.close' );
    _language = _dom.getAttribute( 'lang' );

    const formSubmit = new FormSubmit(
      _dom,
      _notification,
      EmailPopup.BASE_CLASS,
      { validator: emailValidation, language: _language }
    );

    formSubmit.init();

    formSubmit.addEventListener( 'success', _onEmailSignupSuccess );

    _closeElement.addEventListener( 'click', hidePopup );

    return this;
  }

  this.init = init;
  this.hidePopup = hidePopup;
  this.showPopup = showPopup;
  this.getDom = getDom;
  return this;
}
EmailPopup.BASE_CLASS = 'o-email-popup';

module.exports = EmailPopup;
