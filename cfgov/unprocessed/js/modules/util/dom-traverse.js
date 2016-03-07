'use strict';

/**
 * Get the sibling nodes of a dom node.
 *
 * @param {HTMLNode} elem - DOM element to get siblings of.
 * @param {string} selector - a selector string.
 * @returns {Array} List of sibling nodes.
 */
function getSiblings( elem, selector ) {
  var siblings = [];
  var sibling;
  var parent = elem.parentNode;
  var possibleSiblings = parent.querySelectorAll( selector );
  for ( var i = 0, len = possibleSiblings.length; i < len; i++ ) {
    sibling = possibleSiblings[i];
    // Check that sibling is not the original element,
    // and that it shares the same parent.
    if ( sibling !== elem &&
         sibling.parentNode === parent ) {
      siblings[siblings.length] = sibling;
    }
  }
  return siblings;
}

/**
 * Return a list, with an element excluded.
 *
 * @param {NodeList} elems - List of DOM elements.
 * @param {HTMLNode} exclude - DOM element to exlude from elems.
 * @returns {Array} edited elems list or original elems list,
 *   if exlude was not found.
 */
function not( elems, exclude ) {
  var elemsArr = Array.prototype.slice.call( elems );
  var index = elemsArr.indexOf( exclude );
  if ( index > -1 ) {
    return elemsArr.splice( index, 1 );
  }
  return elemsArr;
}

/**
 * Get the nearest parent node of an element.
 *
 * @param {HTMLNode} elem - A DOM element.
 * @param {string} selector - CSS selector.
 * @returns {HTMLNode} Nearest parent node that matches the selector.
 */
function closest( elem, selector ) {
  elem = elem.parentNode;

  var matchesSelector = elem.matches ||
                        elem.webkitMatchesSelector ||
                        elem.mozMatchesSelector ||
                        elem.msMatchesSelector;
  var match;

  while ( elem ) {
    if ( matchesSelector.bind( elem )( selector ) ) {
      match = elem;
    } else {
      elem = elem.parentElement;
    }

    if ( match ) return elem;
  }

  return null;
}

module.exports = {
  closest:     closest,
  getSiblings: getSiblings,
  not:         not
};
