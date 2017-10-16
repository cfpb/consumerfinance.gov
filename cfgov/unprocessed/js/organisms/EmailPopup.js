'use strict';

var helpers = require( '../modules/util/email-popup-helpers' );

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

  function hidePopup() {
    _baseElement.classList.remove( VISIBLE_CLASS );
    helpers.recordEmailPopupClosure();
  }

  function showPopup() {
    if ( helpers.showEmailPopup() ) {
      _baseElement.classList.add( VISIBLE_CLASS );
      helpers.recordEmailPopupView();
    }

    return true;
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
