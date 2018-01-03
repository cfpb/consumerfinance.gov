/* eslint no-unused-vars: "off" */


const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;

const AlphaTransition =
  require( BASE_JS_PATH + 'modules/transition/AlphaTransition' );

const HTML_SNIPPET = '<div class="content-1"></div>';

describe( 'AlphaTransition', () => {
  let transition;

  // DOM-related settings.
  let document;
  let contentDom;

  before( () => {
    this.jsdom = require( 'jsdom-global' )( HTML_SNIPPET );
    document = window.document;
    contentDom = document.querySelector( '.content-1' );
  } );

  beforeEach( () => {
    transition = new AlphaTransition( contentDom );
    transition.init();
  } );

  after( () => this.jsdom() );

  describe( '.fadeIn()', () => {
    it( 'should return instance of AlphaTransition', () => {
      expect( transition.fadeIn() ).to.be.instanceof( AlphaTransition );
    } );

    it( 'should apply u-alpha-100 class', () => {
      transition.fadeIn();
      const classes = 'content-1 u-alpha-transition u-alpha-100';
      expect( contentDom.className ).to.equal( classes );
    } );
  } );

  describe( '.fadeOut()', () => {
    it( 'should return instance of AlphaTransition', () => {
      expect( transition.fadeOut() ).to.be.instanceof( AlphaTransition );
    } );

    it( 'should apply u-alpha-0 class', () => {
      transition.fadeOut();
      const classes = 'content-1 u-alpha-transition u-alpha-0';
      expect( contentDom.className ).to.equal( classes );
    } );
  } );
} );
