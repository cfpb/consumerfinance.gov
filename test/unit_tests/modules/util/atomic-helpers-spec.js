'use strict';

const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;
const jsdom = require( 'jsdom' );

const atomicHelpers = require( BASE_JS_PATH + 'modules/util/atomic-helpers' );

describe( 'atomic-helpers', () => {

  const HTML_SNIPPET = '<div class="container">' +
                       '<div class="o-expandable"></div></div>';
  const initdom = jsdom.jsdom( HTML_SNIPPET );
  const document = initdom.defaultView.document;

  let containerDom;
  let expandableDom;

  before( () => {
    containerDom = document.querySelector( '.container' );
    expandableDom = document.querySelector( '.o-expandable' );
  } );

  describe( '.checkDom()', () => {
    it( 'should throw an error if element DOM not found', () => {
      const errMsg = 'null is not valid. ' +
                     'Check that element is a DOM node with ' +
                     'class ".o-expandable"';
      function errFunc() {
        atomicHelpers.checkDom( null, '.o-expandable' );
      }
      expect( errFunc ).to.throw( Error, errMsg );
    } );

    it( 'should throw an error if element class not found', () => {
      const errMsg = 'mock-class not found on or in passed DOM node.';
      function errFunc() {
        atomicHelpers.checkDom( expandableDom, 'mock-class' );
      }
      expect( errFunc ).to.throw( Error, errMsg );
    } );

    it( 'should return the correct HTMLElement when direct element is searched',
    () => {
      const dom = atomicHelpers.checkDom( expandableDom, 'o-expandable' );
      expect( dom ).to.be.equal( expandableDom );
    } );

    it( 'should return the correct HTMLElement when parent element is searched',
    () => {
      const dom = atomicHelpers.checkDom( containerDom, 'o-expandable' );
      expect( dom ).to.be.equal( expandableDom );
    } );
  } );

  describe( '.instantiateAll()', () => {
    xit( 'should return an array of instances', () => {
      // TODO: Implement test.
    } );
  } );

  describe( '.setInitFlag()', () => {
    it( 'should return true when init flag is set', () => {
      expect( atomicHelpers.setInitFlag( expandableDom ) ).to.be.true;
    } );

    it( 'should return false when init flag is already set', () => {
      atomicHelpers.setInitFlag( expandableDom );
      expect( atomicHelpers.setInitFlag( expandableDom ) ).to.be.false;
    } );
  } );

  describe( '.destroyInitFlag()', () => {

    beforeEach( function() {
      atomicHelpers.setInitFlag( expandableDom );
    } );

    it( 'should return true when init flag is removed', () => {
      expect( atomicHelpers.destroyInitFlag( expandableDom ) ).to.be.true;
    } );

    it( 'should return false when init flag has already been removed', () => {
      atomicHelpers.destroyInitFlag( expandableDom );
      expect( atomicHelpers.destroyInitFlag( expandableDom ) ).to.be.false;
    } );
  } );
} );
