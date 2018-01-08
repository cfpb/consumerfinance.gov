const BASE_JS_PATH = '../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;
const Tree = require( BASE_JS_PATH + 'modules/Tree' );

describe( 'Tree', () => {
  let tree;

  beforeEach( () => {
    tree = new Tree();
  } );

  describe( '.init()', () => {
    it( 'should have a proper state before initialization', () => {
      expect( tree instanceof Tree ).to.be.true;
      expect( tree.getRoot() ).to.be.null;
      expect( tree.getAllAtLevel( 0 ) instanceof Array ).to.be.true;
      expect( tree.getAllAtLevel( 0 ).length ).to.equal( 0 );
    } );

    it( 'should have a proper state after initialization', () => {
      expect( tree.init( 'R' ) instanceof Tree ).to.be.true;
      expect( tree.getRoot().constructor.name === 'TreeNode' ).to.be.true;
      expect( tree.getAllAtLevel( 0 ) instanceof Array ).to.be.true;
    } );
  } );

  describe( '.getRoot()', () => {
    it( 'should have a properly initialized root node', () => {
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

  describe( '.getAllAtLevel()', () => {
    it( 'should return the root level', () => {
      tree.init( 'R' );
      const nodeR = tree.getRoot();
      expect( tree.getAllAtLevel( 0 )[0] ).to.equal( nodeR );
    } );

    /**
     * Make this Tree:
     *        R
     *       / \
     *      A   B
     */
    it( 'should return the first level', () => {
      tree.init( 'R' );
      const nodeR = tree.getRoot();
      const nodeA = tree.add( 'A', nodeR );
      const nodeB = tree.add( 'B', nodeR );
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
    it( 'should return the second level', () => {
      tree.init( 'R' );
      const nodeR = tree.getRoot();
      const nodeA = tree.add( 'A', nodeR );
      const nodeB = tree.add( 'B', nodeR );
      const nodeC = tree.add( 'C', nodeA );
      expect( tree.getAllAtLevel( 0 )[0] ).to.equal( nodeR );
      expect( tree.getAllAtLevel( 1 )[0] ).to.equal( nodeA );
      expect( tree.getAllAtLevel( 1 )[1] ).to.equal( nodeB );
      expect( tree.getAllAtLevel( 2 )[0] ).to.equal( nodeC );
    } );
  } );

  describe( '.add()', () => {
    it( 'should have a properly initialzed child node', () => {
      tree.init( 'R' );
      const nodeR = tree.getRoot();
      const nodeA = tree.add( 'A', nodeR );
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

  describe( '.remove()', () => {
    xit( 'should have a properly initialized tree', () => {
      // TODO: Implement tree.remove() method.
    } );
  } );
} );
