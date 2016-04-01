'use strict';

var BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

var chai = require( 'chai' );
var expect = chai.expect;
var Tree = require( BASE_JS_PATH + 'modules/Tree' );
var treeTraversal = require( BASE_JS_PATH + 'modules/util/tree-traversal' );

describe( 'Tree traversal', function() {

  var tree;
  var nodeR;
  var nodeA;
  var nodeB;
  var nodeC;
  var nodeD;
  var nodeE;

  /**
   * Make this Tree:
   *        R
   *       / \
   *      A   B
   *    / | \
   *   C  D  E
   */
  beforeEach( function() {
    tree = new Tree();
    tree.init( 'R' );
    nodeR = tree.getRoot();
    nodeA = tree.add( 'A', nodeR );
    nodeB = tree.add( 'B', nodeR );
    nodeC = tree.add( 'C', nodeA );
    nodeD = tree.add( 'D', nodeA );
    nodeE = tree.add( 'E', nodeA );
  } );

  describe( 'backtrack', function() {
    it( 'should traverse up the tree', function() {
      var nodes = [];
      var that;
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

  describe( 'breadth-first search', function() {
    it( 'should traverse down the tree', function() {
      var nodes = [];
      var that;
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

  describe( 'depth-first search', function() {
    it( 'should traverse down the tree', function() {
      var nodes = [];
      var that;
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
