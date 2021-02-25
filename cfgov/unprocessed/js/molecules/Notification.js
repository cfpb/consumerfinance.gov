// Required modules.
import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import SUCCESS_ICON from '@cfpb/cfpb-icons/src/icons/check-round.svg';
import WARNING_ICON from '@cfpb/cfpb-icons/src/icons/warning-round.svg';
import ERROR_ICON from '@cfpb/cfpb-icons/src/icons/error-round.svg';

/**
 * Constants for the state of this Notification.
 */
const SUCCESS = 'success';
const WARNING = 'warning';
const ERROR = 'error';

const ICON = {};
ICON[SUCCESS] = SUCCESS_ICON;
ICON[WARNING] = WARNING_ICON;
ICON[ERROR] = ERROR_ICON;

const BASE_CLASS = 'm-notification';
// Constants for the Notification modifiers.
const MODIFIER_VISIBLE = `${ BASE_CLASS }__visible`;

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
  const _dom = checkDom( element, BASE_CLASS );
  const _contentDom = _dom.querySelector( '.' + BASE_CLASS + '_content' );

  let _currentType;

  /**
   * @returns {Notification} An instance.
   */
  function init() {
    if ( !setInitFlag( _dom ) ) {
      return this;
    }

    // Check and set default type of notification.
    const classList = _dom.classList;
    if ( classList.contains( `${ BASE_CLASS }__${ SUCCESS }` ) ) {
      _currentType = SUCCESS;
    } else if ( classList.contains( `${ BASE_CLASS }__${ WARNING }` ) ) {
      _currentType = WARNING;
    } else if ( classList.contains( `${ BASE_CLASS }__${ ERROR }` ) ) {
      _currentType = ERROR;
    }

    return this;
  }

  /**
   * @param {number} type - The notification type.
   * @param {string} messageText - The content of the notification message.
   * @param {string} [explanationText] -
   *   The content of the notification explanation.
   * @returns {Notification} An instance.
   */
  function update( type, messageText, explanationText ) {
    _setType( type );
    _setContent( messageText, explanationText );

    return this;
  }

  /**
   * @param {string} messageText - The content of the notification message.
   * @param {string} [explanationText] -
   *   The content of the notification explanation.
   * @returns {Notification} An instance.
   */
  function _setContent( messageText, explanationText ) {
    let content = `
      <div class="h4 m-notification_message">
        ${ messageText }
      </div>`;
    if ( typeof explanationText !== 'undefined' ) {
      content += `
        <p class="m-notification_explanation">
          ${ explanationText }
        </p>`;
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

    // If this is an unsupported notification type, throw an error.
    if ( type !== SUCCESS && type !== WARNING && type !== ERROR ) {
      throw new Error( `${ type } is not a supported notification type!` );
    }

    const classList = _dom.classList;
    classList.remove( BASE_CLASS + '__' + _currentType );
    classList.add( `${ BASE_CLASS }__${ type }` );
    _currentType = type;

    // Replace <svg> element with contents of type_ICON.
    const currentIcon = _dom.querySelector( '.cf-icon-svg' );
    const newIconSetup = document.createElement( 'div' );
    newIconSetup.innerHTML = ICON[type];
    const newIcon = newIconSetup.firstChild;

    _dom.replaceChild( newIcon, currentIcon );

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

  this.init = init;
  this.show = show;
  this.hide = hide;
  this.update = update;

  return this;
}

Notification.BASE_CLASS = BASE_CLASS;
Notification.SUCCESS = SUCCESS;
Notification.WARNING = WARNING;
Notification.ERROR = ERROR;

export default Notification;
