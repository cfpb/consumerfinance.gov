import {
  DESKTOP,
  MOBILE,
  TABLET,
  getBreakpoint,
  viewportIsIn
} from '../../../../../cfgov/unprocessed/js/modules/util/breakpoint-state';
import varsBreakpoints from '@cfpb/cfpb-core/src/vars-breakpoints';

let configKeys;

describe( 'breakpoint-state', () => {
  beforeEach( () => {
    configKeys = Object.keys( varsBreakpoints );
  } );

  describe( '.getBreakpoint()', () => {
    it( 'should return an object with properties from config file', () => {
      const breakpointStatekeys =
        Object.keys( varsBreakpoints ).map( key => {
          key.replace( 'is', '' );
          key.charAt( 0 ).toLowerCase() + key.slice( 1 );
          return key;
        } );

      expect( getBreakpoint() instanceof Object ).toBe( true );
      expect( configKeys.sort().join() === breakpointStatekeys.sort().join() )
        .toBe( true );
    } );

    it( 'should return an object with one state property set to true', () => {
      let trueValueCount = 0;

      const breakpointStateGet = getBreakpoint();
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

          expect( getBreakpoint( width )[rangeKey] )
            .toBe( true );
        }
      }
    } );

  } );

  describe( '.viewportIsIn()', () => {
    it( 'should determine whether inside desktop breakpoint threshold', () => {
      expect( viewportIsIn( DESKTOP ) ).toBe( true );

      /* TODO:
         Mock getBreakpoint() to return a small breakpoint size,
         so that viewportIsIn( DESKTOP ) returns false and can be tested with
         expect( viewportIsIn( DESKTOP ) ).toBe( false ); */
    } );

    it( 'should determine whether inside tablet breakpoint threshold', () => {
      expect( viewportIsIn( TABLET ) ).toBe( false );

      /* TODO:
         Mock getBreakpoint() to return a tablet breakpoint size,
         so that viewportIsIn( TABLET ) returns true and can be tested with
         expect( viewportIsIn( TABLET ) ).toBe( true ); */
    } );

    it( 'should determine whether inside tablet breakpoint threshold', () => {
      expect( viewportIsIn( MOBILE ) ).toBe( false );

      /* TODO:
         Mock getBreakpoint() to return a mobile breakpoint size,
         so that viewportIsIn( MOBILE ) returns true and can be tested with
         expect( viewportIsIn( MOBILE ) ).toBe( true ); */
    } );
  } );

} );
