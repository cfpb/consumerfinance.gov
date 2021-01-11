// Required modules.
import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import EventObserver from '@cfpb/cfpb-atomic-component/src/mixins/EventObserver.js';
import MaxHeightTransition from '../modules/transition/MaxHeightTransition.js';
import FlyoutMenu from '../modules/behavior/FlyoutMenu.js';
import { DESKTOP, TABLET, viewportIsIn } from '../modules/util/breakpoint-state.js';

const BASE_CLASS = 'o-summary-mobile';

/**
 * SummaryMobile
 * @class
 *
 * @classdesc Initializes a new SummaryMobile organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {SummaryMobile} An instance.
 */
function SummaryMobile( element ) {
  const _dom = checkDom( element, BASE_CLASS );
  const _contentDom = _dom.querySelector( `.${ BASE_CLASS }_content` );
  const _btnDom = _dom.querySelector( `.${ BASE_CLASS }_btn` );
  let _transition;
  let _flyout;

  // Whether the menu has been expanded or not.
  let _isExpanded = false;

  // Whether this instance's behaviors are suspended or not.
  let _suspended = true;

  /**
   * @returns {SummaryMobile} An instance.
   */
  function init() {
    if ( !setInitFlag( _dom ) ) {
      return this;
    }

    _transition = new MaxHeightTransition( _contentDom ).init();
    _flyout = new FlyoutMenu( _dom ).init();

    _resizeHandler();

    window.addEventListener( 'resize', _resizeHandler );
    // Pipe window resize handler into orientation change on supported devices.
    if ( 'onorientationchange' in window ) {
      window.addEventListener( 'orientationchange', _resizeHandler );
    }

    return this;
  }

  /**
   * Handle resizing of the window,
   * suspends or resumes the mobile or desktop menu behaviors.
   */
  function _resizeHandler() {
    if ( viewportIsIn( DESKTOP ) || viewportIsIn( TABLET ) ) {
      _suspend();
    } else {
      _resume();
    }
  }

  /**
   * After the summary opens, remove the "read more" button.
   */
  function _expandEndHandler() {
    _hideButton();
    _isExpanded = true;
  }

  function _showButton() {
    _btnDom.classList.remove( 'u-hidden' );
  }

  function _hideButton() {
    _btnDom.classList.add( 'u-hidden' );
  }

  /**
   * Add events necessary for the desktop menu behaviors.
   * @returns {boolean} Whether it has successfully been resumed or not.
   */
  function _resume() {
    if ( _suspended && _isExpanded === false ) {
      _flyout.addEventListener( 'expandEnd', _expandEndHandler );
      // Set resume state.
      _transition.setElement( _contentDom );
      _flyout.setExpandTransition( _transition, _transition.maxHeightDefault );
      _flyout.setCollapseTransition( _transition, _transition.maxHeightSummary );
      _transition.animateOff();
      _transition.maxHeightSummary();
      _transition.animateOn();
      _showButton();

      _suspended = false;
    }

    return !_suspended;
  }

  /**
   * Remove events necessary for the desktop menu behaviors.
   * @returns {boolean} Whether it has successfully been suspended or not.
   */
  function _suspend() {
    if ( !_suspended ) {
      _suspended = true;
      _flyout.removeEventListener( 'expandEnd', _expandEndHandler );
      _flyout.clearTransitions();
    }

    return _suspended;
  }

  // Attach public events.
  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.init = init;

  return this;
}

SummaryMobile.BASE_CLASS = BASE_CLASS;

export default SummaryMobile;
