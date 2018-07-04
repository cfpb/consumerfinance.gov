import Tree from './Tree';

/**
 * TreeDomModel
 * @class
 *
 * @classdesc A tree data structure.
 * Trees have one root node, and child nodes that branch.
 * Like:
 * @returns {TreeDomModel} An instance.
 */
function TreeDomModel() {

  let _tree;

  /**
   * @param {HTMLNode} dom - A dom tree to copy into a tree model.
   * @param {Object} data - Data to attach to the root node.
   * @param {Function} procFunc - Function to call on each dom node.
   * @returns {TreeDomModel} An instance.
   */
  function init( dom, data, selector, procFunc ) {
    _tree = new Tree();
    _tree.init( data );
    _populateTreeFromDom( dom, _tree.getRoot(), selector, procFunc );

    return this;
  }

  /**
   * Perform a recursive depth-first search of the DOM
   * and call a function for each node.
   * @param {HTMLNode} dom - A DOM element to search from.
   * @param {TreeNode} parentNode
   *   Node in a tree from which to attach new nodes.
   * @param {TreeNode} selector
   *   A CSS selector to check that DOM nodes match against,
   *   if they match, include the node in the tree.
   * @param {Function} callback - Function to call on each node.
   */
  function _populateTreeFromDom( dom, parentNode, selector, callback ) {
    const children = dom.children;
    // IE11 does not have children on SVG nodes.
    if ( !children ) {
      return;
    }
    let child;
    for ( let i = 0, len = children.length; i < len; i++ ) {
      child = children[i];
      let childNode = parentNode;
      // If the element matches the selector, add a tree node and run callback.
      const matchesSelector = _getMatchesMethod( child );
      if ( matchesSelector.bind( child )( selector ) ) {
        childNode = parentNode.tree.add( null, parentNode );
        callback( child, childNode );
      }
      _populateTreeFromDom( child, childNode, selector, callback );
    }
  }

  /**
   * Retrieve the correct Element.matches function.
   * @param {HTMLNode} elem - A DOM element.
   * @return {Function} The Element.matches function available in this browser.
   */
  function _getMatchesMethod( elem ) {
    return elem.matches ||
           elem.webkitMatchesSelector ||
           elem.mozMatchesSelector ||
           elem.msMatchesSelector;
  }

  /**
   * @return {Tree} Tree data structure of dom structure.
   */
  function getTree() {
    return _tree;
  }

  this.init = init;
  this.getTree = getTree;

  return this;
}

module.exports = TreeDomModel;
