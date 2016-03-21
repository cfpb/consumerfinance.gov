'use strict';

/**
 * Perform a backtrack up a Tree to the root.
 * Given this Tree and starting at (C):
 *
 *        R
 *       / \
 *      A   B
 *    / | \
 *   C  D  E
 *
 * Returns (C) -> (A) -> (R).
 *
 * @param {TreeNode} node - Node within a tree to traverse from.
 * @param {Function} callback - Function to call at each node.
 */
function backtrack( node, callback ) {
  // TODO: Check that value of `this` references the expected thing.
  //       It may make sense to have it reference node.tree.
  callback.call( this, node );
  var parent = node.parent;
  if ( parent ) {
    backtrack( parent, callback );
  }
}

/**
 * Perform an iterative breadth-first search of a Tree.
 * Given this Tree and starting at (R):
 *
 *        R
 *       / \
 *      A   B
 *    / | \
 *   C  D  E
 *
 * Returns (R) -> (A) -> (B) -> (C) -> (D) -> (E).
 *
 * @param {TreeNode} node - Node within a tree to traverse from.
 * @param {Function} callback - Function to call at each node.
 */
function bfs( node, callback ) {
  var queue = [ node ];
  var currNode;
  var children;
  while( queue.length > 0 ) {
    currNode = queue.shift();
    children = currNode.children;
    if ( children.length > 0 ) {
      queue = queue.concat( children );
    }
    callback.call( this, currNode );
  }
}

/**
 * Perform a recursive depth-first search of a Tree.
 * Given this Tree and starting at (R):
 *
 *        R
 *       / \
 *      A   B
 *    / | \
 *   C  D  E
 *
 * Returns (R) -> (A) -> (C) -> (D) -> (E) -> (B).
 *
 * @param {TreeNode} node - Node within a tree to traverse from.
 * @param {Function} callback - Function to call at each node.
 */
function dfs( node, callback ) {
  // TODO: Check that value of `this` references the expected thing.
  //       It may make sense to have it reference node.tree.
  callback.call( this, node );
  var children = node.children;
  for ( var i = 0, len = children.length; i < len; i++ ) {
    dfs( children[i], callback );
  }
}

module.exports = {
  backtrack: backtrack,
  bfs:       bfs,
  dfs:       dfs
};
