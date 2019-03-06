import * as breakpointState from '../../../../../cfgov/unprocessed/js/modules/util/breakpoint-state';
import breakpointsConfig from 'cf-core/src/cf-vars-breakpoints';

let configKeys;

describe( 'breakpoint-state', () => {
  beforeEach( () => {
    configKeys = Object.keys( breakpointsConfig );
  } );

  describe( '.get()', () => {
    it( 'should return an object with properties from config file', () => {
      const breakpointStatekeys =
        Object.keys( breakpointsConfig ).map( key => {
          key.replace( 'is', '' );
          key.charAt( 0 ).toLowerCase() + key.slice( 1 );
          return key;
        } );

      expect( breakpointState.get() instanceof Object ).toBe( true );
      expect( configKeys.sort().join() === breakpointStatekeys.sort().join() )
        .toBe( true );
    } );

    it( 'should return an object with one state property set to true', () => {
      let trueValueCount = 0;

      const breakpointStateGet = breakpointState.get();
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
      for ( rangeKey in breakpointsConfig ) {
        width = breakpointsConfig[rangeKey].max ||
                breakpointsConfig[rangeKey].min;
        breakpointStateKey =
          'is' + rangeKey.charAt( 0 ).toUpperCase() + rangeKey.slice( 1 );

        expect( breakpointState.get( width )[breakpointStateKey] ).toBe( true );
      }
    } );

  } );

  describe( '.isInDesktop()', () => {
    it( 'should determine whether inside desktop breakpoint threshold', () => {
      expect( breakpointState.isInDesktop() ).toBe( true );

      /* TODO:
         Mock breakpointState.get() to return a small breakpoint size, so
         that breakpointState.isInDesktop() returns false and can be tested with
         expect( breakpointState.isInDesktop() ).toBe( false ); */
    } );
  } );

} );
