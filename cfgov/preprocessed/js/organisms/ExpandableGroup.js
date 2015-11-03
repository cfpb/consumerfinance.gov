'use strict';

// Required polyfills for <IE9.
require( '../modules/polyfill/query-selector' );
require( '../modules/polyfill/event-listener' );

var Expandable = require( '../molecules/Expandable' );

/**
 * ExpandableGroup
 * @class
 *
 * @classdesc Initializes a new Expandable Group organism.
 *
 * @param {Object} context
 *   The DOM element within which to search for the organism.
 * @returns {Object} An ExpandableGroup instance.
 */
function ExpandableGroup( context ) {

  var _dom = context.classList.contains( 'expandable-group' ) ?
             context : context.querySelector( '.expandable-group' );
  var _domChildren = _dom.querySelectorAll( '.expandable' );
  var _lastOpenChild;
  var _isAccordion;

  /**
   * @returns {Object} The ExpandableGroup instance.
   */
  function init() {
    _isAccordion = _dom.getAttribute( 'data-accordion' ) === 'True';

    var child;
    var len = _domChildren.length;

    for ( var i = 0; i < len; i++ ) {
      child = new Expandable( _domChildren[i] ).init();
      child.addEventListener( 'beginExpand', _childOpened );
    }

    return this;
  }

  /**
   * Handle opening event of a child Expandable instance.
   * @param {Object} ev An object that references the event target.
   */
  function _childOpened( ev ) {
    if ( _isAccordion ) {
      if ( _lastOpenChild ) {
        _lastOpenChild.collapse();
      }
      _lastOpenChild = ev.target;
    }
  }

  this.init = init;
  return this;
}

module.exports = ExpandableGroup;
