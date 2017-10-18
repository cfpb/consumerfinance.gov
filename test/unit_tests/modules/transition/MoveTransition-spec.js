/* eslint no-unused-vars: "off" */

'use strict';

const BASE_JS_PATH = '../../../../cfgov/unprocessed/js/';

const chai = require( 'chai' );
const expect = chai.expect;
const jsdom = require( 'jsdom' );

const MoveTransition =
  require( BASE_JS_PATH + 'modules/transition/MoveTransition' );

describe( 'MoveTransition', () => {

  let transition;

  // DOM-related settings.
  let initdom;
  let document;
  const HTML_SNIPPET = '<div class="content-1"></div>';
  let contentDom;

  beforeEach( () => {
    initdom = jsdom.jsdom( HTML_SNIPPET );
    document = initdom.defaultView.document;
    contentDom = document.querySelector( '.content-1' );
    transition = new MoveTransition( contentDom );
    transition.init();
  } );

  describe( '.moveToOrigin()', () => {
    it( 'should return instance of MoveTransition', () => {
      expect( transition.moveToOrigin() ).to.be.instanceof( MoveTransition );
    } );

    it( 'should apply u-move-to-origin class', () => {
      transition.moveToOrigin();
      const classes = 'content-1 u-move-transition u-move-to-origin';
      expect( contentDom.className ).to.equal( classes );
    } );
  } );

  describe( '.moveRight()', () => {
    it( 'should return instance of MoveTransition', () => {
      expect( transition.moveRight() ).to.be.instanceof( MoveTransition );
    } );

    it( 'should apply u-move-to-origin class', () => {
      transition.moveRight();
      const classes = 'content-1 u-move-transition u-move-right';
      expect( contentDom.className ).to.equal( classes );
    } );
  } );

  describe( '.moveUp()', () => {
    it( 'should return instance of MoveTransition', () => {
      expect( transition.moveUp() ).to.be.instanceof( MoveTransition );
    } );

    it( 'should apply u-move-to-origin class', () => {
      transition.moveUp();
      const classes = 'content-1 u-move-transition u-move-up';
      expect( contentDom.className ).to.equal( classes );
    } );
  } );

  describe( '.moveLeft()', () => {
    it( 'should return instance of MoveTransition', () => {
      expect( transition.moveUp() ).to.be.instanceof( MoveTransition );
    } );

    it( 'should apply u-move-left class', () => {
      transition.moveLeft();
      const classes = 'content-1 u-move-transition u-move-left';
      expect( contentDom.className ).to.equal( classes );
    } );

    it( 'should apply u-move-left-2x class', () => {
      transition.moveLeft( 2 );
      const classes = 'content-1 u-move-transition u-move-left-2x';
      expect( contentDom.className ).to.equal( classes );
    } );

    it( 'should apply u-move-left-3x class', () => {
      transition.moveLeft( 3 );
      const classes = 'content-1 u-move-transition u-move-left-3x';
      expect( contentDom.className ).to.equal( classes );
    } );

    it( 'should throw error when move left range is out-of-range', () => {

      function checkMoveLeftOutOfRange() {
        return transition.moveLeft( 4 );
      }
      expect( checkMoveLeftOutOfRange ).to.throw( 'MoveTransition: moveLeft count is out of range!' );
    } );
  } );
} );
