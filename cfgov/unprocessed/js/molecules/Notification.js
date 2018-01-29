// Required modules.
const atomicHelpers = require( '../modules/util/atomic-helpers' );
const standardType = require( '../modules/util/standard-type' );
const SUCCESS_ICON = require(
  'svg-inline-loader!../../../../node_modules/cf-icons/src/icons/check-round.svg'
);
const WARNING_ICON = require(
  'svg-inline-loader!../../../../node_modules/cf-icons/src/icons/warning-round.svg'
);
const ERROR_ICON = require(
  'svg-inline-loader!../../../../node_modules/cf-icons/src/icons/error-round.svg'
);

const ICON = {
  success: SUCCESS_ICON,
  warning: WARNING_ICON,
  error:   ERROR_ICON
};

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
function Notification( element ) {

  const BASE_CLASS = 'm-notification';

  /**
   * Constants for the state of this Notification.
   * If these change, the keys in the ICON object above must be updated to match
   */
  const SUCCESS = 'success';
  const WARNING = 'warning';
  const ERROR = 'error';

  // Constants for the Notification modifiers.
  const MODIFIER_VISIBLE = BASE_CLASS + '__visible';

  const _dom = atomicHelpers.checkDom( element, BASE_CLASS );
  const _contentDom = _dom.querySelector( '.' + BASE_CLASS + '_content' );

  let _currentType;

  /**
   * @returns {Notification|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }

    // Check and set default type of notification.
    const classList = _dom.classList;
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
   * @param {number} type The notification type.
   * @param {string} messageText The content of the notification message.
   * @param {string|HTMLNode} explanationText
   *   The content of the notification explanation.
   * @returns {Notification} An instance.
   */
  function setTypeAndContent( type, messageText, explanationText ) {
    _setType( type );
    setContent( messageText, explanationText );

    return this;
  }

  /**
   * @param {string} messageText The content of the notification message.
   * @param {string|HTMLNode} explanationText
   *   The content of the notification explanation.
   * @returns {Notification} An instance.
   */
  function setContent( messageText, explanationText ) {
    let content = '<p class="h4 m-notification_message">' +
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
   * @param {number} type The notification type.
   * @returns {Notification} An instance.
   */
  function _setType( type ) {
    // If type hasn't changed, return.
    if ( _currentType === type ) {
      return this;
    }

    const classList = _dom.classList;
    classList.remove( BASE_CLASS + '__' + _currentType );

    if ( type === SUCCESS ||
         type === WARNING ||
         type === ERROR ) {
      classList.add( BASE_CLASS + '__' + type );
      _currentType = type;

      // Replace <svg> element with contents of type_ICON
      const currentIcon = _dom.querySelector( '.cf-icon-svg' );
      const newIcon = document.createRange().createContextualFragment(
        ICON[type]
      );
      _dom.replaceChild( newIcon, currentIcon );
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
