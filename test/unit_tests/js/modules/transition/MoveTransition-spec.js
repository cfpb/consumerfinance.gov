import MoveTransition from '../../../../../cfgov/unprocessed/js/modules/transition/MoveTransition';

let transition;

// DOM-related settings.
let contentDom;

const HTML_SNIPPET = '<div class="content-1"></div>';

describe( 'MoveTransition', () => {
  beforeAll( () => {
    document.body.innerHTML = HTML_SNIPPET;
  } );

  beforeEach( () => {
    contentDom = document.querySelector( '.content-1' );
    transition = new MoveTransition( contentDom );
    transition.init();
  } );

  describe( '.moveToOrigin()', () => {
    it( 'should return instance of MoveTransition', () => {
      expect( transition.moveToOrigin() ).toBeInstanceOf( MoveTransition );
    } );

    it( 'should apply u-move-to-origin class', () => {
      transition.moveToOrigin();
      const classes = 'content-1 u-move-transition u-move-to-origin';
      expect( contentDom.className ).toStrictEqual( classes );
    } );
  } );

  describe( '.moveRight()', () => {
    it( 'should return instance of MoveTransition', () => {
      expect( transition.moveRight() ).toBeInstanceOf( MoveTransition );
    } );

    it( 'should apply u-move-to-origin class', () => {
      transition.moveRight();
      const classes = 'content-1 u-move-transition u-move-right';
      expect( contentDom.className ).toStrictEqual( classes );
    } );
  } );

  describe( '.moveUp()', () => {
    it( 'should return instance of MoveTransition', () => {
      expect( transition.moveUp() ).toBeInstanceOf( MoveTransition );
    } );

    it( 'should apply u-move-to-origin class', () => {
      transition.moveUp();
      const classes = 'content-1 u-move-transition u-move-up';
      expect( contentDom.className ).toStrictEqual( classes );
    } );
  } );

  describe( '.moveLeft()', () => {
    it( 'should return instance of MoveTransition', () => {
      expect( transition.moveUp() ).toBeInstanceOf( MoveTransition );
    } );

    it( 'should apply u-move-left class', () => {
      transition.moveLeft();
      const classes = 'content-1 u-move-transition u-move-left';
      expect( contentDom.className ).toStrictEqual( classes );
    } );

    it( 'should apply u-move-left-2x class', () => {
      transition.moveLeft( 2 );
      const classes = 'content-1 u-move-transition u-move-left-2x';
      expect( contentDom.className ).toStrictEqual( classes );
    } );

    it( 'should apply u-move-left-3x class', () => {
      transition.moveLeft( 3 );
      const classes = 'content-1 u-move-transition u-move-left-3x';
      expect( contentDom.className ).toStrictEqual( classes );
    } );

    it( 'should throw error when move left range is out-of-range', () => {

      function checkMoveLeftOutOfRange() {
        return transition.moveLeft( 4 );
      }
      expect( checkMoveLeftOutOfRange )
        .toThrow( 'MoveTransition: moveLeft count is out of range!' );
    } );
  } );
} );
