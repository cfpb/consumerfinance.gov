// Required modules.
import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import EventObserver from '@cfpb/cfpb-atomic-component/src/mixins/EventObserver.js';
import MaxHeightTransition from '@cfpb/cfpb-atomic-component/src/utilities/transition/MaxHeightTransition.js';
import FlyoutMenu from '../modules/behavior/FlyoutMenu.js';
import { DESKTOP, TABLET, viewportIsIn } from '../modules/util/breakpoint-state.js';

const BASE_CLASS = 'o-summary';

/**
 * Summary
 * @class
 *
 * @classdesc Initializes a new Summary organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {Summary} An instance.
 */
function Summary( element ) {
  const _dom = checkDom( element, BASE_CLASS );
  const _hasMobileModifier = _dom.classList.contains( `${ BASE_CLASS }__mobile` );
  const _contentDom = _dom.querySelector( `.${ BASE_CLASS }_content` );
  const _btnDom = _dom.querySelector( `.${ BASE_CLASS }_btn` );
  let _transition;
  let _flyout;

  // Whether the menu has been expanded or not.
  let _isExpanded = false;

  // Whether this instance's behaviors are suspended or not.
  let _suspended = true;

  /**
   * @returns {Summary} An instance.
   */
  function init() {
    if ( !setInitFlag( _dom ) ) {
      return this;
    }

    /* Bail out of initializatiion if the height of the summary's content
       is less then our summary height of 5.5ems (16 * 5.5 = 88)
       See https://github.com/cfpb/design-system/blob/72623270013f2ad08dbe92b5b709ed2b434ee41e/packages/cfpb-atomic-component/src/utilities/transition/transition.less#L84 */
    if ( _contentDom.offsetHeight <= 88 ) {
      _hideButton();
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

    /* When we click inside the content area we may be changing the size,
       such as when a video player expands on being clicked.
       So, let's refresh the transition to recalculate the max-height,
       just in case. */
    _contentDom.addEventListener( 'click', _contentClicked );

    return this;
  }

  /**
   * Handler for when the content area is clicked.
   * Refresh the transition to recalculate the max-height.
   * @param {MouseEvent} evt - the mouse event object.
   */
  function _contentClicked( evt ) {
    /* We don't need to refresh if a link was clicked as we'll be navigating
       to another page. */
    if ( evt.target.tagName !== 'A' ) {
      _transition.refresh();
    }
  }

  /**
   * Handle resizing of the window,
   * suspends or resumes the mobile or desktop menu behaviors.
   */
  function _resizeHandler() {
    if ( _hasMobileModifier &&
         viewportIsIn( DESKTOP ) || viewportIsIn( TABLET ) ) {
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
    // Re-initialize the transition on every resize to set the max-height.
    _transition.refresh();

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

Summary.BASE_CLASS = BASE_CLASS;

export default Summary;
