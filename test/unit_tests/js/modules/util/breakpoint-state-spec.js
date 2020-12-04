import {
  DESKTOP,
  MOBILE,
  TABLET,
  getBreakpointState,
  viewportIsIn
} from '../../../../../cfgov/unprocessed/js/modules/util/breakpoint-state';
import varsBreakpoints from '@cfpb/cfpb-core/src/vars-breakpoints';

let configKeys;

/**
 * Change the viewport to width x height. Mocks window.resizeTo( w, h ).
 * @param  {number} width - width in pixels.
 * @param  {number} height - height in pixels.
 */
function windowResizeTo( width, height ) {
  // Change the viewport to width x height. Mocks window.resizeTo( w, h ).
  global.innerWidth = width;
  global.innerHeight = height;

  // Trigger the window resize event.
  global.dispatchEvent( new Event( 'resize' ) );
}

/**
 * @param  {number} size - Font size to set for the base body font size.
 */
function setBaseFontSize( size ) {
  global.document.body.outerHTML = `
    <body style="font-size: ${ size }px;"></body>
  `;
}

describe( 'breakpoint-state', () => {
  describe( '.viewportIsIn()', () => {
    beforeEach( () => {
      setBaseFontSize( 16 );
    } );

    it( 'should determine whether inside desktop breakpoint threshold', () => {
      windowResizeTo( 1200, 800 );
      expect( viewportIsIn( DESKTOP ) ).toBe( true );
      windowResizeTo( 599, 800 );
      expect( viewportIsIn( DESKTOP ) ).toBe( false );
    } );

    it( 'should determine whether inside tablet breakpoint threshold', () => {
      windowResizeTo( 1200, 800 );
      expect( viewportIsIn( TABLET ) ).toBe( false );
      windowResizeTo( 899, 800 );
      expect( viewportIsIn( TABLET ) ).toBe( true );
    } );

    it( 'should determine whether inside tablet breakpoint threshold', () => {
      windowResizeTo( 1200, 800 );
      expect( viewportIsIn( MOBILE ) ).toBe( false );
      windowResizeTo( 599, 800 );
      expect( viewportIsIn( MOBILE ) ).toBe( true );
    } );
  } );

} );
