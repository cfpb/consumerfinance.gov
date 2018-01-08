const FormSubmit = require( './FormSubmit.js' );
const validators = require( '../modules/util/validators' );
const emailHelpers = require( '../modules/util/email-popup-helpers' );
const BASE_CLASS = 'o-email-signup';
const language = document.body.querySelector( '.content' ).lang;

/**
 * EmailPopup
 * @class
 *
 * @classdesc Initializes the organism.
 *
 * @param {string} el
 *   The selector for the organism.
 * @returns {EmailSignup} An instance.
 */
function EmailPopup( el ) {
  const _baseElement = document.querySelector( el );
  const _closeElement = _baseElement.querySelector( '.close' );
  const VISIBLE_CLASS = 'o-email-popup__visible';

  /**
   * Function used to hide popup by removing visible class.
   */
  function hidePopup() {
    _baseElement.classList.remove( VISIBLE_CLASS );
    emailHelpers.recordEmailPopupClosure();
  }

  /**
   * Function used to show popup by adding visible class.
   * @returns {boolean} true.
   */
  function showPopup() {
    if ( emailHelpers.showEmailPopup() ) {
      _baseElement.classList.add( VISIBLE_CLASS );
      emailHelpers.recordEmailPopupView();
    }

    return true;
  }

  /**
   * Function used to validate email address.
   * @param {object} fields An object containing form fields.
   * @returns {object} Validation status.
   */
  function emailValidation( fields ) {

    return validators.email(
      fields.email,
      '',
      { language: language }
    ).msg;
  }

  /**
   * Callback function invoked after successful email submission.
   * @param {event} event Click event.
   *
   */
  function _onEmailSignupSuccess( event ) {
    const form = event.form;
    const input = form.querySelector( 'input[name="code"]' );
    const code = input.value;

    if ( code === 'USCFPB_128' ) {
      emailHelpers.recordEmailRegistration();
    }
  }

  /**
   * Function used to instatiate and initialize components.
   */
  function init() {
    const formSubmit = new FormSubmit(
      _baseElement.querySelector( '.' + BASE_CLASS ),
      BASE_CLASS,
      { validator: emailValidation, language: language }
    );

    formSubmit.init();

    formSubmit.addEventListener( 'success', _onEmailSignupSuccess );

    _closeElement.addEventListener( 'click', hidePopup );
  }

  this.init = init;
  this.hidePopup = hidePopup;
  this.showPopup = showPopup;
  this.el = _baseElement;
  return this;
}

module.exports = EmailPopup;
