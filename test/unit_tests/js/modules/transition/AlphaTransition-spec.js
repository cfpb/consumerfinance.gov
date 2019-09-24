import AlphaTransition from '../../../../../unprocessed/js/modules/transition/AlphaTransition';

let transition;

// DOM-related settings.
let contentDom;

const HTML_SNIPPET = '<div class="content-1"></div>';

describe( 'AlphaTransition', () => {
  beforeAll( () => {
    document.body.innerHTML = HTML_SNIPPET;
    contentDom = document.querySelector( '.content-1' );
  } );

  beforeEach( () => {
    transition = new AlphaTransition( contentDom );
    transition.init();
  } );

  describe( '.fadeIn()', () => {
    it( 'should return instance of AlphaTransition', () => {
      expect( transition.fadeIn() ).toBeInstanceOf( AlphaTransition );
    } );

    it( 'should apply u-alpha-100 class', () => {
      transition.fadeIn();
      let classes = 'content-1 u-alpha-transition u-is-animating u-alpha-100';
      expect( contentDom.className ).toStrictEqual( classes );
      transition.addEventListener( 'transitionend', () => {
        classes = 'content-1 u-alpha-transition u-alpha-100';
        expect( contentDom.className ).toStrictEqual( classes );
      } );
    } );
  } );

  describe( '.fadeOut()', () => {
    it( 'should return instance of AlphaTransition', () => {
      expect( transition.fadeOut() ).toBeInstanceOf( AlphaTransition );
    } );

    it( 'should apply u-alpha-0 class', () => {
      transition.fadeOut();
      let classes = 'content-1 u-alpha-transition u-is-animating u-alpha-0';
      expect( contentDom.className ).toStrictEqual( classes );
      transition.addEventListener( 'transitionend', () => {
        classes = 'content-1 u-alpha-transition u-alpha-0';
        expect( contentDom.className ).toStrictEqual( classes );
      } );
    } );
  } );
} );
