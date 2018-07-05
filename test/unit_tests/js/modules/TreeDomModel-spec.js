const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';
const TreeDomModel = require( BASE_JS_PATH + 'modules/TreeDomModel' );
const Tree = require( BASE_JS_PATH + 'modules/Tree' );

const HTML_SNIPPET = `
<div id="R" data-js-hook="test-node">
  <div id="container">
    <div id="A" data-js-hook="test-node">
      <div id="C" data-js-hook="test-node"></div>
    </div>
    <div id="B" data-js-hook="test-node"></div>
  </div>
  <svg></svg>
</div>
`;

describe( 'TreeDomModel', () => {
  let model;
  let rootDomNode;
  const rootMockData = {};

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    rootDomNode = document.querySelector( '#R' );
    model = new TreeDomModel();
  } );

  describe( '.init()', () => {
    it( 'should have a proper state before initialization', () => {
      expect( model instanceof TreeDomModel ).toBe( true );
      expect( model.getTree() ).toBeUndefined();
    } );

    it( 'should have a properly initialized', () => {
      model.init( rootDomNode, rootMockData, 'div', () => {
        // Empty node process function.
      } );
      expect( model.getTree() instanceof Tree ).toBe( true );
    } );
  } );

  describe( '.getTree()', () => {
    /**
     * Test this Tree:
     *        R
     *       / \
     *      A   B
     *    /
     *   C
     */
    it( 'should have a properly initialized tree', () => {
      let id = 0;
      model.init( rootDomNode, rootMockData, '[data-js-hook=test-node]',
        ( dom, node ) => {
          // This is mock data that's checked in the expectations below.
          node.data = ++id;
        } );
      const tree = model.getTree();
      const root = tree.getRoot();
      const A = root.children[0];
      const B = root.children[1];
      const C = A.children[0];
      expect( root.data ).toBe( rootMockData );
      expect( A.data ).toBe( 1 );
      expect( B.data ).toBe( 3 );
      expect( C.data ).toBe( 2 );
    } );
  } );
} );
