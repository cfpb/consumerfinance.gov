import
domTools
  from '../../../../../../cfgov/unprocessed/apps/owning-a-home/js/form-explainer/dom-tools';

const HTML_SNIPPET = `
<div id="test"></div>
<div id="test2" class="test"></div>
<div class="test"></div>
<div class="test"></div>
`;

let testDom;
let testDomList;

describe( 'dom-tools', () => {

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    testDom = document.querySelector( '#test' );
    testDomList = document.querySelectorAll( '.test' );
  } );

  describe( 'applyAll()', () => {
    it( 'should apply a function to an element or list of elements', () => {
      const testFunc = () => {
        // Empty function for testing.
      };
      expect( domTools.applyAll( 'wrong', testFunc ) ).toBe( false );
      expect( domTools.applyAll( testDom, testFunc ) ).toBe( true );
      expect( domTools.applyAll( testDomList, testFunc ) ).toBe( true );
    } );

    it( 'should create a div containing arbitrary HTML', () => {
      expect( domTools.createElement( HTML_SNIPPET ).outerHTML ).toBe(
        '<div id="test"></div>'
      );
    } );
  } );

  describe( 'hasClass()', () => {
    it( 'should return true when element has provided class', () => {
      const dom = document.querySelector( '.test' );
      expect( domTools.hasClass( dom, 'test' ) ).toBe( true );
      // hasClass takes both a selector and a dom node.
      expect( domTools.hasClass( '#test2', 'test' ) ).toBe( true );
    } );

    it( 'should return false when element ' +
        'does not have provided class', () => {
      const dom = document.querySelector( '.test' );
      expect( domTools.hasClass( dom, 'example' ) ).toBe( false );
      // hasClass takes both a selector and a dom node.
      expect( domTools.hasClass( '#test2', 'example' ) ).toBe( false );
    } );
  } );
} );
