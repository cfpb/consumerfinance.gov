const BASE_JS_PATH = '../../../../../cfgov/unprocessed/js/';
const dataSet = require( BASE_JS_PATH + 'modules/util/data-set' ).dataSet;

let baseDom;

const HTML_SNIPPET = `
  <div data-test-value-a="testValueA"
       data-test-value-B="testValueB"
       data-testValue-C="testValueC"
       data-test-ValuE-D="testValueD"
       data-TEST-value-E="testValueE">
    testValue
  </div>
`;

describe( 'data-set', () => {
  beforeAll( () => {
    document.body.innerHTML = HTML_SNIPPET;
    baseDom = document.querySelector( 'div' );
  } );

  describe( 'dataset attribute is supported', () => {
    it( 'should have the correct keys and values when using utility', () => {
      const dataset = dataSet( baseDom );
      expect( dataset.testValueA ).toBe( 'testValueA' );
      expect( dataset.testValueB ).toBe( 'testValueB' );
      expect( dataset.testvalueC ).toBe( 'testValueC' );
      expect( dataset.testValueD ).toBe( 'testValueD' );
      expect( dataset.testValueE ).toBe( 'testValueE' );
    } );
  } );

  describe( 'dataset attribute is NOT supported', () => {
    it( 'should have the correct keys and values when using utility', () => {
      // Removes dataset from jsdom by setting dataset to undefined.
      Object.defineProperty(document.documentElement, 'dataset', {});

      const dataset = dataSet( baseDom );
      expect( dataset.testValueA ).toBe( 'testValueA' );
      expect( dataset.testValueB ).toBe( 'testValueB' );
      expect( dataset.testvalueC ).toBe( 'testValueC' );
      expect( dataset.testValueD ).toBe( 'testValueD' );
      expect( dataset.testValueE ).toBe( 'testValueE' );
    } );
  } );
} );
