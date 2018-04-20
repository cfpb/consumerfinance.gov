const BASE_JS_PATH = '../../../../../cfgov/unprocessed/apps/owning-a-home/';
const domTools = require( BASE_JS_PATH + 'js/dom-tools.js' ).default;

const HTML_SNIPPET = `
  <div id="test"></div>
  <div class="test"></div>
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
        `<div id="test"></div>`
      );
    } );
  } );
} );
