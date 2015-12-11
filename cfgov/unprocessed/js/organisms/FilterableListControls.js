'use strict';

// Required modules.
var atomicCheckers = require( '../modules/util/atomic-checkers' );
var Expandable = require( '../molecules/Expandable' );

/**
 * FilterableListControls
 * @class
 *
 * @classdesc Initializes a new Filterable-List-Controls organism.
 *
 * @param {HTMLNode} element The DOM element within which to search for the organism.
 */
function FilterableListControls( element ) {
  var BASE_CLASS = 'o-filterable-list-controls';

  var _dom = atomicCheckers.validateDomElement( element, BASE_CLASS, 'FilterableListControls' );
  var _expandable = new Expandable( _dom ).init();
}

module.exports = FilterableListControls;
