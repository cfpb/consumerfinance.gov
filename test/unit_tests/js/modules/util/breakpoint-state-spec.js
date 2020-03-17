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

describe( 'breakpoint-state', () => {
  beforeEach( () => {
    configKeys = Object.keys( varsBreakpoints );
  } );

  describe( '.getBreakpointState()', () => {
    it( 'should return an object with properties from config file', () => {
      const breakpointStatekeys =
        Object.keys( varsBreakpoints ).map( key => {
          key.replace( 'is', '' );
          key.charAt( 0 ).toLowerCase() + key.slice( 1 );
          return key;
        } );

      expect( getBreakpointState() instanceof Object ).toBe( true );
      expect( configKeys.sort().join() === breakpointStatekeys.sort().join() )
        .toBe( true );
    } );

    it( 'should return an object with one state property set to true', () => {
      let trueValueCount = 0;

      const breakpointStateGet = getBreakpointState();
      // eslint-disable-next guard-for-in
      let stateKey;
      for ( stateKey in breakpointStateGet ) {
        if ( breakpointStateGet[stateKey] === true ) trueValueCount++;
      }

      expect( trueValueCount === 1 ).toBe( true );
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

  } );

  describe( '.viewportIsIn()', () => {
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
