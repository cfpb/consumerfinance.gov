import * as treeTraversal from '../../../../../cfgov/unprocessed/js/modules/util/tree-traversal';
import Tree from '../../../../../cfgov/unprocessed/js/modules/Tree';

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

      expect( that ).toStrictEqual( treeTraversal );
      expect( nodes[0] ).toStrictEqual( nodeC );
      expect( nodes[1] ).toStrictEqual( nodeA );
      expect( nodes[2] ).toStrictEqual( nodeR );
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

      expect( that ).toStrictEqual( treeTraversal );
      expect( nodes[0] ).toStrictEqual( nodeR );
      expect( nodes[1] ).toStrictEqual( nodeA );
      expect( nodes[2] ).toStrictEqual( nodeB );
      expect( nodes[3] ).toStrictEqual( nodeC );
      expect( nodes[4] ).toStrictEqual( nodeD );
      expect( nodes[5] ).toStrictEqual( nodeE );
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

      expect( that ).toStrictEqual( treeTraversal );
      expect( nodes[0] ).toStrictEqual( nodeR );
      expect( nodes[1] ).toStrictEqual( nodeA );
      expect( nodes[2] ).toStrictEqual( nodeC );
      expect( nodes[3] ).toStrictEqual( nodeD );
      expect( nodes[4] ).toStrictEqual( nodeE );
      expect( nodes[5] ).toStrictEqual( nodeB );
    } );
  } );

} );
