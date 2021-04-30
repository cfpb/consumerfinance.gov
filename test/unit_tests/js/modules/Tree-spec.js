import Tree from '../../../../cfgov/unprocessed/js/modules/Tree.js';

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
      expect( tree.getAllAtLevel( 0 ).length ).toStrictEqual( 0 );
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
      expect( tree.getRoot().tree ).toStrictEqual( tree );
      expect( tree.getRoot().data ).toStrictEqual( 'R' );
      expect( tree.getRoot().parent ).toBeUndefined();
      expect( tree.getRoot().children.length ).toStrictEqual( 0 );
      expect( tree.getRoot().level ).toStrictEqual( 0 );
    } );
  } );

  describe( '.getAllAtLevel()', () => {
    it( 'should return the root level', () => {
      tree.init( 'R' );
      const nodeR = tree.getRoot();
      expect( tree.getAllAtLevel( 0 )[0] ).toStrictEqual( nodeR );
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
      expect( tree.getAllAtLevel( 0 )[0] ).toStrictEqual( nodeR );
      expect( tree.getAllAtLevel( 1 )[0] ).toStrictEqual( nodeA );
      expect( tree.getAllAtLevel( 1 )[1] ).toStrictEqual( nodeB );
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
      expect( tree.getAllAtLevel( 0 )[0] ).toStrictEqual( nodeR );
      expect( tree.getAllAtLevel( 1 )[0] ).toStrictEqual( nodeA );
      expect( tree.getAllAtLevel( 1 )[1] ).toStrictEqual( nodeB );
      expect( tree.getAllAtLevel( 2 )[0] ).toStrictEqual( nodeC );
    } );
  } );

  describe( '.add()', () => {
    it( 'should have a properly initialzed child node', () => {
      tree.init( 'R' );
      const nodeR = tree.getRoot();
      const nodeA = tree.add( 'A', nodeR );
      expect( nodeA ).not.toBeNull();
      expect( nodeA.constructor.name === 'TreeNode' ).toBe( true );
      expect( nodeA.tree ).toStrictEqual( tree );
      expect( nodeA.data ).toStrictEqual( 'A' );
      expect( nodeA.parent ).toStrictEqual( nodeR );
      expect( nodeA.children.length ).toStrictEqual( 0 );
      expect( nodeA.level ).toStrictEqual( 1 );
      expect( nodeR.children[0] ).toStrictEqual( nodeA );
      expect( tree.getAllAtLevel( 0 ).length ).toStrictEqual( 1 );
      expect( tree.getAllAtLevel( 1 ).length ).toStrictEqual( 1 );
    } );
  } );
} );
