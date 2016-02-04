'use strict';

// Required polyfills for IE9.
if ( !Modernizr.classlist ) { require( '../modules/polyfill/class-list' ); } // eslint-disable-line no-undef, global-require, no-inline-comments, max-len

// Required modules.
var atomicCheckers = require( '../modules/util/atomic-checkers' );

/**
 * Notification
 * @class
 *
 * @classdesc Initializes a new Notification molecule.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the molecule.
 * @returns {Object} An Notification instance.
 */
function Notification( element ) { // eslint-disable-line max-statements, inline-comments, max-len

  var BASE_CLASS = 'm-notification';

  // Constants for the state of this Notification.
  var SUCCESS = 'success';
  var WARNING = 'warning';
  var ERROR = 'error';

  // Constants for the Notification modifiers.
  var MODIFIER_VISIBLE = BASE_CLASS + '__visible';

  var _dom =
    atomicCheckers.validateDomElement( element, BASE_CLASS, 'Notification' );
  var _contentDom = _dom.querySelector( '.' + BASE_CLASS + '_content' );

  var _currentType;

  /**
   * @returns {Object} The Notification instance.
   */
  function init() {
    // Check and set default type of notification.
    var classList = _dom.classList;
    if ( classList.contains( BASE_CLASS + '__' + SUCCESS ) ) {
      _currentType = SUCCESS;
    } else if ( classList.contains( BASE_CLASS + '__' + WARNING ) ) {
      _currentType = WARNING;
    } else if ( classList.contains( BASE_CLASS + '__' + ERROR ) ) {
      _currentType = ERROR;
    }

    return this;
  }

  /**
   * @param {number} type The notifiation type.
   * @param {string} messageText The content of the notifiation message.
   * @param {string|HTMLNode} explanationText
   *   The content of the notifiation explanation.
   * @returns {Object} The Notification instance.
   */
  function setTypeAndContent( type, messageText, explanationText ) {
    _setType( type );
    setContent( messageText, explanationText );

    return this;
  }

  /**
   * @param {string} messageText The content of the notifiation message.
   * @param {string|HTMLNode} explanationText
   *   The content of the notifiation explanation.
   * @returns {Object} The Notification instance.
   */
  function setContent( messageText, explanationText ) {
    var content = '<p class="h4">' +
                  messageText +
                  '</p>';
    if ( typeof explanationText !== 'undefined' ) {
      content += '<p class="h4 m-notification_explanation">' +
                 explanationText +
                 '</p>';
    }
    _contentDom.innerHTML = content;

    return this;
  }

  /**
   * @param {number} type The notifiation type.
   * @returns {Object} The Notification instance.
   */
  function _setType( type ) {
    // If type hasn't changed, return.
    if ( _currentType === type ) {
      return this;
    }

    var classList = _dom.classList;
    classList.remove( BASE_CLASS + '__' + _currentType );

    if ( type === SUCCESS ||
         type === WARNING ||
         type === ERROR ) {
      classList.add( BASE_CLASS + '__' + type );
      _currentType = type;
    } else {
      throw new Error( type + ' is not a supported notification type!' );
    }

    return this;
  }

  /**
   * @returns {Object} The Notification instance.
   */
  function show() {
    if ( _currentType === ERROR || _currentType === WARNING ) {
      _contentDom.setAttribute( 'role', 'alert' );
    } else {
      _contentDom.removeAttribute( 'role' );
    }
    _dom.classList.add( MODIFIER_VISIBLE );
    return this;
  }

  /**
   * @returns {Object} The Notification instance.
   */
  function hide() {
    _dom.classList.remove( MODIFIER_VISIBLE );
    return this;
  }

  this.SUCCESS = SUCCESS;
  this.WARNING = WARNING;
  this.ERROR = ERROR;

  this.init = init;
  this.setContent = setContent;
  this.setTypeAndContent = setTypeAndContent;
  this.show = show;
  this.hide = hide;

  return this;
}

module.exports = Notification;
