'use strict';

var helpers = require( '../modules/util/email-popup-helpers' );
var AlphaTransition = require( '../modules/transition/AlphaTransition' );

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
  var transition = new AlphaTransition( _baseElement ).init();

  function hidePopup() {
    transition.fadeOut();
    helpers.recordEmailPopupClosure();
  }

  function showPopup() {
    if ( helpers.showEmailPopup() ) {
      transition.fadeIn();
      helpers.recordEmailPopupView();
    }

    return true
  }

  function init() {
    _closeElement.addEventListener( 'click', hidePopup );
  }

  this.init = init;
  this.hidePopup = hidePopup;
  this.showPopup = showPopup;
  this.el = _baseElement;
  return this;
}

module.exports = EmailPopup;
