const BASE_JS_PATH = '../../../../../cfgov/unprocessed/js/';
const dataSet = require( BASE_JS_PATH + 'modules/util/data-set' ).dataSet;
const chai = require( 'chai' );
const expect = chai.expect;

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
      expect( dataset.testValueA ).to.equal( 'testValueA' );
      expect( dataset.testValueB ).to.equal( 'testValueB' );
      expect( dataset.testvalueC ).to.equal( 'testValueC' );
      expect( dataset.testValueD ).to.equal( 'testValueD' );
      expect( dataset.testValueE ).to.equal( 'testValueE' );
    } );
  } );

  describe( 'dataset attribute is NOT supported', () => {
    it( 'should have the correct keys and values when using utility', () => {

      /* Removes dataset from jsdom by setting dataset to undefined.
         document = {}; // eslint-disable-line no-global-assign
         document.documentElement = {}; */
      delete document.documentElement.dataset;

      const dataset = dataSet( baseDom );
      expect( dataset.testValueA ).to.equal( 'testValueA' );
      expect( dataset.testValueB ).to.equal( 'testValueB' );
      expect( dataset.testvalueC ).to.equal( 'testValueC' );
      expect( dataset.testValueD ).to.equal( 'testValueD' );
      expect( dataset.testValueE ).to.equal( 'testValueE' );
    } );
  } );
} );
