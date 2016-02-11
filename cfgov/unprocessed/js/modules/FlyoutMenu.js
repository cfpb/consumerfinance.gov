'use strict';

// Required modules.
var EventObserver = require( '../modules/util/EventObserver' );

/**
 * FlyoutMenu
 * @class
 *
 * @classdesc Initializes a new FlyoutMenu molecule.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the molecule.
 * @param {string} triggerSel - The selector for the menu trigger.
 * @param {string} contentSel - The selector for the menu content.
 * @param {string} altTriggerSel - The selector for a second menu trigger.
 * @returns {Object} A FlyoutMenu instance.
 */
function FlyoutMenu( element, triggerSel, contentSel, altTriggerSel ) {

  var _isExpanded = false;

  var _triggerDom = element.querySelector( triggerSel );
  var _contentDom = element.querySelector( contentSel );
  var _altTriggerDom = element.querySelector( altTriggerSel );

  var _transitionEndEvent = _getTransitionEndEvent( _contentDom );
  var _isAnimating = false;

  // Needed to add and remove events to transitions.
  var _expandEndBinded = _expandEnd.bind( this );
  var _collapseEndBinded = _collapseEnd.bind( this );

  /**
   * @returns {Object} The FlyoutMenu instance.
   */
  function init() {
    _triggerDom.addEventListener( 'click', _triggerClicked.bind( this ) );

    if ( altTriggerSel ) {
      _altTriggerDom.addEventListener( 'click', _triggerClicked.bind( this ) );
    }

    return this;
  }

  /**
   * Event handler for when the search input trigger is clicked,
   * which opens/closes the search input.
   * @param {MouseEvent} event - The flyout trigger was clicked.
   */
  function _triggerClicked( event ) {
    event.preventDefault();
    this.dispatchEvent( 'triggerClick', { target: event.target } );
    if ( _isExpanded ) {
      this.collapse();
    } else {
      this.expand();
    }
  }

  /**
   * Open the search box.
   * @returns {Object} A FlyoutMenu instance.
   */
  function expand() {
    if ( !_isExpanded && !_isAnimating ) {
      this.dispatchEvent( 'toggle', { target: this } );
      this.dispatchEvent( 'expandBegin', { target: this } );
      _isExpanded = true;
      _isAnimating = true;
      // If transition is not supported, call handler directly (IE9/OperaMini).
      if ( _transitionEndEvent ) {
        _contentDom.addEventListener( _transitionEndEvent, _expandEndBinded );
      } else {
        _expandEndBinded();
      }
      _triggerDom.setAttribute( 'aria-expanded', 'true' );
      _contentDom.setAttribute( 'aria-expanded', 'true' );
    }

    return this;
  }

  /**
   * Close the search box.
   * @returns {Object} A FlyoutMenu instance.
   */
  function collapse() {
    if ( _isExpanded && !_isAnimating ) {
      this.dispatchEvent( 'toggle', { target: this } );
      this.dispatchEvent( 'collapseBegin', { target: this } );
      _isExpanded = false;
      _isAnimating = true;
      // If transition is not supported, call handler directly (IE9/OperaMini).
      if ( _transitionEndEvent ) {
        _contentDom.addEventListener( _transitionEndEvent, _collapseEndBinded );
      } else {
        _collapseEndBinded();
      }
      _triggerDom.setAttribute( 'aria-expanded', 'false' );
      _contentDom.setAttribute( 'aria-expanded', 'false' );
      _triggerDom.focus();
    }

    return this;
  }

  /**
   * Expand animation has completed.
   */
  function _expandEnd() {
    _isAnimating = false;
    _contentDom.removeEventListener( _transitionEndEvent, _expandEndBinded );
    this.dispatchEvent( 'expandEnd', { target: this } );
  }

  /**
   * Collapse animation has completed.
   */
  function _collapseEnd() {
    _isAnimating = false;
    _contentDom.removeEventListener( _transitionEndEvent, _collapseEndBinded );
    this.dispatchEvent( 'collapseEnd', { target: this } );
  }

  /**
   * @returns {Object}
   *   Hash of trigger, alternative trigger, and content DOM references.
   */
  function _getDom() {
    return {
      altTrigger: _altTriggerDom,
      content:    _contentDom,
      trigger:    _triggerDom
    };
  }

  // Attach public events.
  var eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  this.init = init;
  this.expand = expand;
  this.collapse = collapse;
  this.getDom = _getDom;

  return this;
}

// TODO: Move to a utility module and share this between Expandables and here.
/**
 * @param {HTMLNode} elm
 *   The element to check for support of transition end event.
 * @returns {string} The browser-prefixed transition end event.
 */
function _getTransitionEndEvent( elm ) {
  var transition;
  var transitions = {
    WebkitTransition: 'webkitTransitionEnd',
    MozTransition:    'transitionend',
    OTransition:      'oTransitionEnd otransitionend',
    transition:       'transitionend'
  };

  for ( var t in transitions ) {
    if ( transitions.hasOwnProperty( t ) &&
         typeof elm.style[t] !== 'undefined' ) {
      transition = transitions[t];
      break;
    }
  }
  return transition;
}

module.exports = FlyoutMenu;
