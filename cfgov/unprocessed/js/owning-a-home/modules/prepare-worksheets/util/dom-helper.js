'use strict';

/**
 * Convert arbitary HTML into a HTMLNode, and append it to a parent element.
 * @param {HTMLNode} node - The container to append a child to.
 * @param {string} str - HTML as a raw string.
 * @param {string} elementType - HTML type as a raw string.
 *   Default is 'div'.
 * @returns {HTMLNode} The child that was appended.
 */
this.appendChild = function( node, str, elementType ) {
  var temp = document.createElement( elementType || 'div' );
  temp.innerHTML = str;
  if ( temp.children.length > 1 ) {
    throw new Error( 'Supplied HTML must have one top-level element!' );
  }
  return node.appendChild( temp.children[0] );
};
