'use strict';

var helpers = require( '../modules/util/email-popup-helpers' );

var $ = window.$;

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
  var _baseElement = $( el );
  var _closeElement = $( el ).find( '.close' );

  function hidePopup() {
    _baseElement.fadeOut();
    helpers.recordEmailPopupClosure();
  }

  function showPopup() {
    if ( helpers.showEmailPopup() ) {
      _baseElement.fadeIn();
      helpers.recordEmailPopupView();
    }
  }

  function init() {
    _closeElement.on( 'click', hidePopup );
  }

  this.init = init;
  this.hidePopup = hidePopup;
  this.showPopup = showPopup;
  this.el = _baseElement;
  return this;
}

module.exports = EmailPopup;
