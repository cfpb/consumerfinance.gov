const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;
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

      expect( that ).to.equal( treeTraversal );
      expect( nodes[0] ).to.equal( nodeC );
      expect( nodes[1] ).to.equal( nodeA );
      expect( nodes[2] ).to.equal( nodeR );
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

      expect( that ).to.equal( treeTraversal );
      expect( nodes[0] ).to.equal( nodeR );
      expect( nodes[1] ).to.equal( nodeA );
      expect( nodes[2] ).to.equal( nodeB );
      expect( nodes[3] ).to.equal( nodeC );
      expect( nodes[4] ).to.equal( nodeD );
      expect( nodes[5] ).to.equal( nodeE );
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

      expect( that ).to.equal( treeTraversal );
      expect( nodes[0] ).to.equal( nodeR );
      expect( nodes[1] ).to.equal( nodeA );
      expect( nodes[2] ).to.equal( nodeC );
      expect( nodes[3] ).to.equal( nodeD );
      expect( nodes[4] ).to.equal( nodeE );
      expect( nodes[5] ).to.equal( nodeB );
    } );
  } );

} );
