'use strict';

var helpers = require( '../modules/util/email-popup-helpers' );
var FormSubmit = require( './FormSubmit.js' );
var validators = require( '../modules/util/validators' );
var emailHelpers = require( '../modules/util/email-popup-helpers' );
var BASE_CLASS = 'o-email-signup';
var language = document.body.querySelector( '.content' ).lang;

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
  var _baseElement = document.querySelector( el );
  var _closeElement = _baseElement.querySelector( '.close' );
  var VISIBLE_CLASS = 'o-email-popup__visible';

  /**
   * Function used to hide popup by removing visible class.
   */
  function hidePopup() {
    _baseElement.classList.remove( VISIBLE_CLASS );
    helpers.recordEmailPopupClosure();
  }

  /**
   * Function used to show popup by adding visible class.
   * @returns {boolean} true.
   */
  function showPopup() {
    if ( helpers.showEmailPopup() ) {
      _baseElement.classList.add( VISIBLE_CLASS );
      helpers.recordEmailPopupView();
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
   * @param {event} Click event.
   *
   */
  function _onEmailSignupSuccess( event ) {
    var form = event.form;
    var input = form.querySelector( 'input[name="code"]' );
    var code = input.value;

    if ( code === 'USCFPB_127' ) {
      emailHelpers.recordEmailRegistration();
    }
  }

  /**
   * Function used to instatiate and initialize components.
   */
  function init() {
    var formSubmit = new FormSubmit(
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
