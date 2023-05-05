/**
 * Perform a backtrack up a Tree to the root.
 * Given this Tree and starting at (C):
 *
 * ------ R
 * ----- / \
 * ---- A   B
 * -- / | \
 * - C  D  E
 *
 * Returns (C) -> (A) -> (R).
 * @param {TreeNode} node - Node within a tree to traverse from.
 * @param {Function} callback - Function to call at each node.
 *   `this` will be the treeTranserval module within the callback.
 */
function backtrack(node, callback) {
  callback.call(this, node);
  const parent = node.parent;
  if (parent) {
    backtrack.apply(this, [parent, callback]);
  }
}

/**
 * Perform an iterative breadth-first search of a Tree.
 * Given this Tree and starting at (R):
 *
 * ------ R
 * ----- / \
 * ---- A   B
 * -- / | \
 * - C  D  E
 *
 * Returns (R) -> (A) -> (B) -> (C) -> (D) -> (E).
 * @param {TreeNode} node - Node within a tree to traverse from.
 * @param {Function} callback - Function to call at each node.
 *   `this` will be the treeTranserval module within the callback.
 */
function bfs(node, callback) {
  let queue = [node];
  let currNode;
  let children;
  while (queue.length > 0) {
    currNode = queue.shift();
    children = currNode.children;
    if (children.length > 0) {
      queue = queue.concat(children);
    }
    callback.call(this, currNode);
  }
}

/**
 * Perform a recursive depth-first search of a Tree.
 * Given this Tree and starting at (R):
 *
 * ------ R
 * ----- / \
 * ---- A   B
 * -- / | \
 * - C  D  E
 *
 * Returns (R) -> (A) -> (C) -> (D) -> (E) -> (B).
 * @param {TreeNode} node - Node within a tree to traverse from.
 * @param {Function} callback - Function to call at each node.
 *   `this` will be the treeTranserval module within the callback.
 */
function dfs(node, callback) {
  callback.call(this, node);
  const children = node.children;
  for (let i = 0, len = children.length; i < len; i++) {
    dfs.apply(this, [children[i], callback]);
  }
}

export { backtrack, bfs, dfs };
