'use strict';

var BASE_JS_PATH = '../../../cfgov/unprocessed/js/';

var chai = require( 'chai' );
var expect = chai.expect;
var Tree = require( BASE_JS_PATH + 'modules/Tree' );

describe( 'Tree', function() {
  var tree;

  beforeEach( function() {
    tree = new Tree();
  } );

  describe( '.init()', function() {
    it( 'should have a proper state before initialization', function() {
      expect( tree instanceof Tree ).to.be.true;
      expect( tree.getRoot() ).to.be.null;
      expect( tree.getAllAtLevel( 0 ) instanceof Array ).to.be.true;
      expect( tree.getAllAtLevel( 0 ).length ).to.equal( 0 );
    } );

    it( 'should have a proper state after initialization', function() {
      expect( tree.init( 'R' ) instanceof Tree ).to.be.true;
      expect( tree.getRoot().constructor.name === 'TreeNode' ).to.be.true;
      expect( tree.getAllAtLevel( 0 ) instanceof Array ).to.be.true;
    } );
  } );

  describe( '.getRoot()', function() {
    it( 'should have a properly initialized root node', function() {
      tree.init( 'R' );
      expect( tree.getRoot() ).to.not.be.null;
      expect( tree.getRoot().constructor.name === 'TreeNode' ).to.be.true;
      expect( tree.getRoot().tree ).to.equal( tree );
      expect( tree.getRoot().data ).to.equal( 'R' );
      expect( tree.getRoot().parent ).to.be.undefined;
      expect( tree.getRoot().children.length ).to.equal( 0 );
      expect( tree.getRoot().level ).to.equal( 0 );
    } );
  } );

  describe( '.getAllAtLevel()', function() {
    it( 'should return the root level', function() {
      tree.init( 'R' );
      var nodeR = tree.getRoot();
      expect( tree.getAllAtLevel( 0 )[0] ).to.equal( nodeR );
    } );

    /**
     * Make this Tree:
     *        R
     *       / \
     *      A   B
     */
    it( 'should return the first level', function() {
      tree.init( 'R' );
      var nodeR = tree.getRoot();
      var nodeA = tree.add( 'A', nodeR );
      var nodeB = tree.add( 'B', nodeR );
      expect( tree.getAllAtLevel( 0 )[0] ).to.equal( nodeR );
      expect( tree.getAllAtLevel( 1 )[0] ).to.equal( nodeA );
      expect( tree.getAllAtLevel( 1 )[1] ).to.equal( nodeB );
    } );

    /**
     * Make this Tree:
     *        R
     *       / \
     *      A   B
     *    /
     *   C
     */
    it( 'should return the second level', function() {
      tree.init( 'R' );
      var nodeR = tree.getRoot();
      var nodeA = tree.add( 'A', nodeR );
      var nodeB = tree.add( 'B', nodeR );
      var nodeC = tree.add( 'C', nodeA );
      expect( tree.getAllAtLevel( 0 )[0] ).to.equal( nodeR );
      expect( tree.getAllAtLevel( 1 )[0] ).to.equal( nodeA );
      expect( tree.getAllAtLevel( 1 )[1] ).to.equal( nodeB );
      expect( tree.getAllAtLevel( 2 )[0] ).to.equal( nodeC );
    } );
  } );

  describe( '.add()', function() {
    it( 'should have a properly initialzed child node', function() {
      tree.init( 'R' );
      var nodeR = tree.getRoot();
      var nodeA = tree.add( 'A', nodeR );
      expect( nodeA ).to.not.be.null;
      expect( nodeA.constructor.name === 'TreeNode' ).to.be.true;
      expect( nodeA.tree ).to.equal( tree );
      expect( nodeA.data ).to.equal( 'A' );
      expect( nodeA.parent ).to.equal( nodeR );
      expect( nodeA.children.length ).to.equal( 0 );
      expect( nodeA.level ).to.equal( 1 );
      expect( nodeR.children[0] ).to.equal( nodeA );
      expect( tree.getAllAtLevel( 0 ).length ).to.equal( 1 );
      expect( tree.getAllAtLevel( 1 ).length ).to.equal( 1 );
    } );
  } );

  describe( '.remove()', function() {
    xit( 'should have a properly initialized tree', function() {
      // TODO: Implement tree.remove() method.
    } );
  } );
} );
