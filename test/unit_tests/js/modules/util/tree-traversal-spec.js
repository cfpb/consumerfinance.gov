const BASE_JS_PATH = '../../../../../cfgov/unprocessed/js/';
const Tree = require( BASE_JS_PATH + 'modules/Tree' );
const treeTraversal = require( BASE_JS_PATH + 'modules/util/tree-traversal' );

describe( 'Tree traversal', () => {

  let tree;
  let nodeR;
  let nodeA;
  let nodeB;
  let nodeC;
  let nodeD;
  let nodeE;

  /**
   * Make this Tree:
   *        R
   *       / \
   *      A   B
   *    / | \
   *   C  D  E
   */
  beforeEach( () => {
    tree = new Tree();
    tree.init( 'R' );
    nodeR = tree.getRoot();
    nodeA = tree.add( 'A', nodeR );
    nodeB = tree.add( 'B', nodeR );
    nodeC = tree.add( 'C', nodeA );
    nodeD = tree.add( 'D', nodeA );
    nodeE = tree.add( 'E', nodeA );
  } );

  describe( 'backtrack', () => {
    it( 'should traverse up the tree', () => {
      const nodes = [];
      let that;
      treeTraversal.backtrack( nodeC, function( node ) {
        that = this;
        nodes.push( node );
      } );

      expect( that ).toEqual( treeTraversal );
      expect( nodes[0] ).toEqual( nodeC );
      expect( nodes[1] ).toEqual( nodeA );
      expect( nodes[2] ).toEqual( nodeR );
    } );
  } );

  describe( 'breadth-first search', () => {
    it( 'should traverse down the tree', () => {
      const nodes = [];
      let that;
      treeTraversal.bfs( nodeR, function( node ) {
        that = this;
        nodes.push( node );
      } );

      expect( that ).toEqual( treeTraversal );
      expect( nodes[0] ).toEqual( nodeR );
      expect( nodes[1] ).toEqual( nodeA );
      expect( nodes[2] ).toEqual( nodeB );
      expect( nodes[3] ).toEqual( nodeC );
      expect( nodes[4] ).toEqual( nodeD );
      expect( nodes[5] ).toEqual( nodeE );
    } );
  } );

  describe( 'depth-first search', () => {
    it( 'should traverse down the tree', () => {
      const nodes = [];
      let that;
      treeTraversal.dfs( nodeR, function( node ) {
        that = this;
        nodes.push( node );
      } );

      expect( that ).toEqual( treeTraversal );
      expect( nodes[0] ).toEqual( nodeR );
      expect( nodes[1] ).toEqual( nodeA );
      expect( nodes[2] ).toEqual( nodeC );
      expect( nodes[3] ).toEqual( nodeD );
      expect( nodes[4] ).toEqual( nodeE );
      expect( nodes[5] ).toEqual( nodeB );
    } );
  } );

} );
