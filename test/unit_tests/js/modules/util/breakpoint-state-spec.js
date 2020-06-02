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
  describe( '.getBreakpointState()', () => {
    it( 'should correctly return bpXS state', () => {
      windowResizeTo( 300 );
      expect( getBreakpointState() ).toStrictEqual( { bpLG: false, bpMED: false, bpSM: false, bpXL: false, bpXS: true } );
    } );

    it( 'should correctly return bpSM state', () => {
      windowResizeTo( 700 );
      expect( getBreakpointState() ).toStrictEqual( { bpLG: false, bpMED: false, bpSM: true, bpXL: false, bpXS: false } );
    } );

    it( 'should correctly return bpMED state', () => {
      windowResizeTo( 1000 );
      expect( getBreakpointState() ).toStrictEqual( { bpLG: false, bpMED: true, bpSM: false, bpXL: false, bpXS: false } );
    } );

    it( 'should correctly return bpLG state', () => {
      windowResizeTo( 1100 );
      expect( getBreakpointState() ).toStrictEqual( { bpLG: true, bpMED: false, bpSM: false, bpXL: false, bpXS: false } );
    } );

    it( 'should correctly return bpXL state', () => {
      windowResizeTo( 1300 );
      expect( getBreakpointState() ).toStrictEqual( { bpLG: false, bpMED: false, bpSM: false, bpXL: true, bpXS: false } );
    } );

    it( 'should set the correct state property when passed width', () => {
      let width;
      let breakpointStateKey;

      // eslint-disable-next-line guard-for-in
      let rangeKey;
      for ( rangeKey in varsBreakpoints ) {
        if ( {}.hasOwnProperty.call( varsBreakpoints, rangeKey ) ) {
          width = varsBreakpoints[rangeKey].max ||
                  varsBreakpoints[rangeKey].min;

          expect( getBreakpointState( width )[rangeKey] ).toBe( true );
        }
      }
    } );

    it( 'should correctly handle non-standard base font sizes', () => {
      // Ensure test utility is working.
      setBaseFontSize( 16 );
      expect( window.getComputedStyle( document.body ).fontSize ).toBe( '16px' );
      setBaseFontSize( 24 );
      expect( window.getComputedStyle( document.body ).fontSize ).toBe( '24px' );

      // Test that live code still works with base font size change.
      setBaseFontSize( 16 );
      windowResizeTo( 900 );
      expect( getBreakpointState() ).toStrictEqual( { bpLG: false, bpMED: false, bpSM: true, bpXL: false, bpXS: false } );
      setBaseFontSize( 24 );
      expect( getBreakpointState() ).toStrictEqual( { bpLG: false, bpMED: false, bpSM: false, bpXL: false, bpXS: true } );
    } );

  } );

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
