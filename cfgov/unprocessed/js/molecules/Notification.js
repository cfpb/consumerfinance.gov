'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var standardType = require( '../modules/util/standard-type' );

/**
 * Notification
 * @class
 *
 * @classdesc Initializes a new Notification molecule.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the molecule.
 * @returns {Notification} An instance.
 */
function Notification( element ) { // eslint-disable-line max-statements, inline-comments, max-len

  var BASE_CLASS = 'm-notification';

  // Constants for the state of this Notification.
  var SUCCESS = 'success';
  var WARNING = 'warning';
  var ERROR = 'error';

  // Constants for the Notification modifiers.
  var MODIFIER_VISIBLE = BASE_CLASS + '__visible';

  var _dom = atomicHelpers.checkDom( element, BASE_CLASS );
  var _contentDom = _dom.querySelector( '.' + BASE_CLASS + '_content' );

  var _currentType;

  /**
   * @returns {Notification|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }

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
   * @returns {Notification} An instance.
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
   * @returns {Notification} An instance.
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
   * Generate a string of HTML from the plugin's settings
   * @returns {string} The expanded HTML string
   * Commented out until nedded.

  function generateHTML( settings ) {
    var template = '<div class="m-notification m-notification__{{ state }}" ' +
                         'style="display: none;">' +
                      '<span class="m-notification_icon cf-icon"></span>' +
                      '<div class="m-notification_content">' +
                        '<p class="h4 m-notification_message">' +
                          '{{ message }}' +
                        '</p>' +
                      '</div>' +
                    '</div>';

    var icon = {
      error:   'delete',
      success: 'approved',
      warning: 'error'
    };
    var data = {
      message: settings.message,
      state:   settings.state,
      icon:    icon[settings.state]
    };
    var template = template.replace( /\{\{\s?(.*?)\s?\}\}/g,
      function( match, token ) {
        return data[token] || '';
      }
    );

    return template;
  }
*/

  /**
   * @param {number} type The notifiation type.
   * @returns {Notification} An instance.
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
   * @returns {Notification} An instance.
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
   * @returns {Notification} An instance.
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
