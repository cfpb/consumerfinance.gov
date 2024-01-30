/**
 * Tree
 * @class
 * @classdesc A tree data structure.
 * Trees have one root node, and child nodes that branch.
 * Like:
 *
 * ------ R
 * ----- / \
 * ---- A   B
 * -- / | \
 * - C  D  E
 * @returns {Tree} An instance.
 */
function Tree() {
  let _root = null;
  const _levelCache = {};

  /**
   * @param {object} data - Data to attach to the root node.
   * @returns {Tree} An instance.
   */
  function init(data) {
    _root = new TreeNode(this, data);
    _levelCache[0] = [_root];

    return this;
  }

  /**
   * @param {object} data - Data to attach to new node.
   * @param {TreeNode} parent - Node on which to add a new child node.
   * @returns {TreeNode} The newly instantiated and added node.
   */
  function add(data, parent) {
    const child = new TreeNode(this, data, parent);

    // Save node at each level as a flat array.
    const level = child.level;
    if (_levelCache[level]) {
      _levelCache[level].push(child);
    } else {
      _levelCache[level] = [child];
    }

    parent.children.push(child);

    return child;
  }

  /**
   * @returns {TreeNode} The root node of this Tree.
   */
  function getRoot() {
    return _root;
  }

  /**
   * Get all nodes at a particular tree level. For example, returning
   * Given this Tree and starting at (R):
   *
   * ------ R
   * ----- / \
   * ---- A   B
   * -- / | \
   * - C  D  E
   *
   * Level 0 nodes would return (R).
   * Level 1 nodes would return (A) and (B).
   * Level 2 nodes would return (C), (D), and (E).
   * @param {number} level - The tree level on which to return nodes.
   * @returns {Array} A list of all nodes at a particular tree level.
   */
  function getAllAtLevel(level) {
    let levelCache = _levelCache[level];
    if (!levelCache) levelCache = [];
    return levelCache;
  }

  /* TODO: Implement remove method.
     function remove( child, parent ) {
     } */

  this.add = add;
  this.init = init;
  this.getRoot = getRoot;
  this.getAllAtLevel = getAllAtLevel;

  return this;
}

// PRIVATE CLASS
/**
 * TreeNode
 * @class
 * @classdesc A node in a tree data structure.
 * @param {Tree} tree - The data structure this node is a member of.
 * @param {object} data - The data payload.
 * @param {TreeNode} parent - The parent node in the root,
 *   null if this is the root node.
 * @param {Array} children - List of children nodes.
 * @returns {TreeNode} An instance.
 */
function TreeNode(tree, data, parent, children) {
  this.tree = tree;
  this.data = data;
  this.parent = parent;
  this.children = children || [];
  this.level = parent ? parent.level + 1 : 0;

  return this;
}

export { Tree };
