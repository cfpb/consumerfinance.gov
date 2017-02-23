'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var Expandable = require( '../organisms/Expandable' );
var standardType = require( '../modules/util/standard-type' );

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

  var _dom = atomicHelpers.checkDom( element, BASE_CLASS );
  var _domChildren = _dom.querySelectorAll( '.o-expandable' );
  var _lastOpenChild;
  var _isAccordion;

  /**
   * @returns {ExpandableGroup|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }

    _isAccordion = _dom.classList.contains( BASE_CLASS + '__accordion' );

    var child;
    var len = _domChildren.length;

    for ( var i = 0; i < len; i++ ) {
      child = new Expandable( _domChildren[i] ).init();
      child.addEventListener( 'expandBegin', _childBeginExpand );
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
