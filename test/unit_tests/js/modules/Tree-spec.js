const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const Tree = require( BASE_JS_PATH + 'modules/Tree' );

describe( 'Tree', () => {
  let tree;

  beforeEach( () => {
    tree = new Tree();
  } );

  describe( '.init()', () => {
    it( 'should have a proper state before initialization', () => {
      expect( tree instanceof Tree ).toBe( true );
      expect( tree.getRoot() ).toBeNull();
      expect( tree.getAllAtLevel( 0 ) instanceof Array ).toBe( true );
      expect( tree.getAllAtLevel( 0 ).length ).toEqual( 0 );
    } );

    it( 'should have a proper state after initialization', () => {
      expect( tree.init( 'R' ) instanceof Tree ).toBe( true );
      expect( tree.getRoot().constructor.name === 'TreeNode' ).toBe( true );
      expect( tree.getAllAtLevel( 0 ) instanceof Array ).toBe( true );
    } );
  } );

  describe( '.getRoot()', () => {
    it( 'should have a properly initialized root node', () => {
      tree.init( 'R' );
      expect( tree.getRoot() ).not.toBeNull();
      expect( tree.getRoot().constructor.name === 'TreeNode' ).toBe( true );
      expect( tree.getRoot().tree ).toEqual( tree );
      expect( tree.getRoot().data ).toEqual( 'R' );
      expect( tree.getRoot().parent ).toBeUndefined();
      expect( tree.getRoot().children.length ).toEqual( 0 );
      expect( tree.getRoot().level ).toEqual( 0 );
    } );
  } );

  describe( '.getAllAtLevel()', () => {
    it( 'should return the root level', () => {
      tree.init( 'R' );
      const nodeR = tree.getRoot();
      expect( tree.getAllAtLevel( 0 )[0] ).toEqual( nodeR );
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
      expect( tree.getAllAtLevel( 0 )[0] ).toEqual( nodeR );
      expect( tree.getAllAtLevel( 1 )[0] ).toEqual( nodeA );
      expect( tree.getAllAtLevel( 1 )[1] ).toEqual( nodeB );
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
      expect( tree.getAllAtLevel( 0 )[0] ).toEqual( nodeR );
      expect( tree.getAllAtLevel( 1 )[0] ).toEqual( nodeA );
      expect( tree.getAllAtLevel( 1 )[1] ).toEqual( nodeB );
      expect( tree.getAllAtLevel( 2 )[0] ).toEqual( nodeC );
    } );
  } );

  describe( '.add()', () => {
    it( 'should have a properly initialzed child node', () => {
      tree.init( 'R' );
      const nodeR = tree.getRoot();
      const nodeA = tree.add( 'A', nodeR );
      expect( nodeA ).not.toBeNull();
      expect( nodeA.constructor.name === 'TreeNode' ).toBe( true );
      expect( nodeA.tree ).toEqual( tree );
      expect( nodeA.data ).toEqual( 'A' );
      expect( nodeA.parent ).toEqual( nodeR );
      expect( nodeA.children.length ).toEqual( 0 );
      expect( nodeA.level ).toEqual( 1 );
      expect( nodeR.children[0] ).toEqual( nodeA );
      expect( tree.getAllAtLevel( 0 ).length ).toEqual( 1 );
      expect( tree.getAllAtLevel( 1 ).length ).toEqual( 1 );
    } );
  } );
} );
