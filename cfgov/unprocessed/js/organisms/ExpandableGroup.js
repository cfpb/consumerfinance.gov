'use strict';

// Required polyfills for IE9.
if ( !Modernizr.classlist ) { require( '../modules/polyfill/class-list' ); } // eslint-disable-line no-undef, global-require, no-inline-comments, max-len

// Required modules.
var Expandable = require( '../molecules/Expandable' );
var atomicCheckers = require( '../modules/util/atomic-checkers' );

/**
 * ExpandableGroup
 * @class
 *
 * @classdesc Initializes a new Expandable Group organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {Object} An ExpandableGroup instance.
 */
function ExpandableGroup( element ) {

  var BASE_CLASS = 'o-expandable-group';

  var _dom =
    atomicCheckers.validateDomElement( element, BASE_CLASS, 'ExpandableGroup' );
  var _domChildren = _dom.querySelectorAll( '.m-expandable' );
  var _lastOpenChild;
  var _isAccordion;

  /**
   * @returns {Object} The ExpandableGroup instance.
   */
  function init() {
    _isAccordion = _dom.classList.contains( BASE_CLASS + '__accordion' );

    var child;
    var len = _domChildren.length;

    for ( var i = 0; i < len; i++ ) {
      child = new Expandable( _domChildren[i] ).init();
      child.addEventListener( 'beginExpand', _childBeginExpand );
    }

    return this;
  }

  /**
   * Handle opening event of a child Expandable instance.
   * @param {Object} ev An object that references the event target.
   */
  function _childBeginExpand( ev ) {
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
