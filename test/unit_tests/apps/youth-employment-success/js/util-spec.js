import {
  UNDEFINED,
  actionCreator,
  assign,
  combineReducers
} from '../../../../../cfgov/unprocessed/apps/youth-employment-success/js/util';

const reducerStateA = {
  name: 'barbara',
  location: 'pittsburgh'
};
const reducerStateB = {
  job: 'engineer'
};

const reducerA = ( () => ( state = reducerStateA, action ) => {
  const { type, data } = action;

  switch ( type ) {
    case 'UPDATE_LOCATION': {
      return {
        ...state,
        location: data
      };
    }
    default:
      return state;
  }
} )();

const reducerB = ( () => ( state = reducerStateB, action ) => {
  const { type, data } = action;

  switch ( type ) {
    case 'UPDATE_JOB':
      return {
        ...state,
        job: data
      };
    default:
      return state;
  }
} )();

describe( 'YES utility functions', () => {
  describe( 'action', () => {
    const actionType = 'MY_ACTION';

    it( 'returns a curried function', () => {
      expect( typeof actionCreator( actionType ) === 'function' ).toBeTruthy();
    } );

    it( 'returns an action object when the curried fn is called', () => {
      const data = 'hello';
      const actionObj = actionCreator( actionType )( data );

      expect( actionObj.type ).toBe( actionType );
      expect( actionObj.data ).toBe( data );
    } );
  } );

  describe( 'assign', () => {
    const originalObject = {
      agency: 'CFPB'
    };

    it( 'merges a single object', () => {
      const sourceObj = { team: 'D and D' };
      const nextObj = assign( originalObject, sourceObj );

      expect( nextObj.agency ).toBe( originalObject.agency );
      expect( nextObj.team ).toBe( sourceObj.team );
    } );

    it( 'merges multiple objects', () => {
      const team = { team: 'engineering' };
      const guild = { guild: 'front-end' };
      const merged = assign( originalObject, team, guild );

      expect( merged.team ).toBe( team.team );
      expect( merged.guild ).toBe( guild.guild );
      expect( merged.agency ).toBe( originalObject.agency );
    } );

    it( 'overwrites properties of the original object', () => {
      const override = { agency: 'GSA' };
      expect( assign( originalObject, override ).agency ).toBe( override.agency );
    } );

    it( 'does not mutate the original object', () => {
      expect( assign( originalObject ) ).not.toBe( originalObject );
    } );
  } );

  describe( '.combineReducers()', () => {
    describe( 'invalid usage', () => {
      it( 'throws an error if not passed an object', () => {
        expect( () => combineReducers( reducerA )
        ).toThrow();
      } );

      it( 'throws an error when a reducer does not return state', () => {
        expect( () => combineReducers( {
          a: reducerA,
          b: () => UNDEFINED
        } )()
        ).toThrow();
      } );
    } );

    const reducerMap = {
      a: reducerA,
      b: reducerB
    };
    let reducer;

    beforeAll( () => {
      reducer = combineReducers( reducerMap );
    } );

    it( 'accepts multiple reducer functions and returns a function', () => {
      expect( typeof reducer === 'function' ).toBeTruthy();
    } );

    it( 'properly reduces when it receives actions', () => {
      const location = 'cleveland';
      const nextState = reducer( UNDEFINED, {
        type: 'UPDATE_LOCATION',
        data: location
      } );

      expect( nextState.a ).toEqual( {
        ...reducerStateA,
        location
      } );

      expect( nextState.b ).toEqual( reducerStateB );
    } );
  } );
} );
