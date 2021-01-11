import MaxHeightTransition from '../../../../../cfgov/unprocessed/js/modules/transition/MaxHeightTransition.js';

let transition;

// DOM-related settings.
let contentDom;

const HTML_SNIPPET = '<div class="content-1"></div>';

describe( 'MaxHeightTransition', () => {
  beforeAll( () => {
    document.body.innerHTML = HTML_SNIPPET;
    contentDom = document.querySelector( '.content-1' );
  } );

  beforeEach( () => {
    transition = new MaxHeightTransition( contentDom );
    transition.init();
  } );

  describe( '.maxHeightDefault()', () => {
    it( 'should return instance of MaxHeightTransition', () => {
      expect( transition.maxHeightDefault() ).toBeInstanceOf( MaxHeightTransition );
    } );

    it( 'should apply u-max-height-default class', () => {
      transition.maxHeightSummary();
      let classes = 'content-1 u-max-height-transition u-is-animating u-max-height-summary';
      expect( contentDom.className ).toStrictEqual( classes );
      transition.maxHeightDefault();
      transition.addEventListener( 'transitionend', () => {
        classes = 'content-1 u-max-height-transition u-max-height-default';
        expect( contentDom.className ).toStrictEqual( classes );
      } );
    } );
  } );

  describe( '.maxHeightSummary()', () => {
    it( 'should return instance of MaxHeightTransition', () => {
      expect( transition.maxHeightSummary() ).toBeInstanceOf( MaxHeightTransition );
    } );

    it( 'should apply u-max-height-summary class', () => {
      transition.maxHeightDefault();
      let classes = 'content-1 u-max-height-transition u-is-animating u-max-height-default';
      expect( contentDom.className ).toStrictEqual( classes );
      transition.maxHeightSummary();
      transition.addEventListener( 'transitionend', () => {
        classes = 'content-1 u-max-height-transition u-max-height-summary';
        expect( contentDom.className ).toStrictEqual( classes );
      } );
    } );
  } );


  describe( '.maxHeightZero()', () => {
    it( 'should return instance of MaxHeightTransition', () => {
      expect( transition.maxHeightZero() ).toBeInstanceOf( MaxHeightTransition );
    } );

    it( 'should apply u-max-height-zero class', () => {
      transition.maxHeightDefault();
      let classes = 'content-1 u-max-height-transition u-is-animating u-max-height-default';
      expect( contentDom.className ).toStrictEqual( classes );
      transition.maxHeightZero();
      transition.addEventListener( 'transitionend', () => {
        classes = 'content-1 u-max-height-transition u-max-height-zero';
        expect( contentDom.className ).toStrictEqual( classes );
      } );
    } );
  } );
} );
