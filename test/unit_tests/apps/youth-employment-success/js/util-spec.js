import {
  UNDEFINED,
  actionCreator,
  assign,
  combineReducers,
  entries,
  formatNegative,
  toArray,
  toPrecision,
  toggleCFNotification
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
  describe( 'actionCreator', () => {
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
      expect( assign( originalObject, override ).agency )
        .toBe( override.agency );
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

  describe( '.entries', () => {
    it( 'throws an error when it receives a value that isn\'t an object', () => {
      const invalidArgs = [ function() { return 'a'; }, null, 1, 'bad', [] ];

      invalidArgs.forEach(
        invalidArg => expect( () => entries( invalidArg ) ).toThrow()
      );
    } );

    it( 'reduces an object into an array of arays form key/value pairs', () => {
      const pet = {
        name: 'buddy',
        type: 'cat'
      };

      const objectEntries = entries( pet );

      expect( objectEntries[0][0] ).toBe( 'name' );
      expect( objectEntries[0][1] ).toBe( pet.name );
      expect( objectEntries[1][0] ).toBe( 'type' );
      expect( objectEntries[1][1] ).toBe( pet.type );
    } );
  } );

  describe( '.toArray', () => {
    it( 'turns array-like values into arrays', () => {
      const number = toArray( 1 );
      expect( number.length ).toBe( 0 );

      const string = toArray( 'ab' );
      expect( string.length ).toBe( 2 );
      expect( string[0] ).toBe( 'a' );

      const obj = toArray( {} );
      expect( obj.length ).toBe( 0 );

      const fragment = document.createDocumentFragment();
      const children = [ document.createElement( 'a' ), document.createElement( 'a' ) ];
      children.forEach( child => fragment.appendChild( child ) );

      const dom = document.createElement( 'div' );
      dom.appendChild( fragment );
      const array = toArray( dom.querySelectorAll( 'a' ) );

      expect( array.slice ).toBeDefined();
    } );
  } );

  describe( '.toggleCFNotification', () => {
    it( 'throws an error if first arg is supplied and value is not a dom node', () => {
      expect( () => toggleCFNotification( 'foo', true ) ).toThrow();
    } );

    it( 'toggles a supplied notification', () => {
      const HTML = '<div class="m-notification"></div>';
      document.body.innerHTML = HTML;
      const el = document.querySelector( '.m-notification' );

      toggleCFNotification( el, true );

      expect( el.classList.contains( 'm-notification__visible' ) ).toBeTruthy();

      toggleCFNotification( el, false );

      expect( el.classList.contains( 'm-notification__visible' ) ).toBeFalsy();
    } );
  } );

  describe( '.toPrecision', () => {
    it( 'returns the value if it cant be coerced into a number', () => {
      expect( toPrecision( 'string' ) ).toBe( 'string' );
    } );

    it( 'returns the original number when a precision is not specified', () => {
      const num = '100';
      expect( toPrecision( num ) ).toBe( num );
    } );

    it( 'returns a string of 0 when no arguments are supplied', () => {
      expect( toPrecision() ).toBe( '0' );
    } );

    it( 'adds a number of zeros to the end of a string commesurate with the value supplied as the second argument', () => {
      const string = '100.';

      expect( toPrecision( string, 3 ) ).toBe( '100.000' );
      expect( toPrecision( '100.1', 2 ) ).toBe( '100.10' );
      expect( toPrecision( '100.00', 2 ) ).toBe( '100.00' );
    } );
  } );

  describe( '.formatNegative', () => {
    it( 'returns the value supplied if that value is not a number', () => {
      expect( formatNegative( '-' ) ).toBe( '-' );
    } );

    it( 'adds an html entity minus to a number', () => {
      expect( formatNegative( '-1600' ) ).toBe( '&#8722;1600' );
    } );

    it( 'preserves decimals', () => {
      expect( formatNegative( '-1600.00' ) ).toBe( '&#8722;1600.00' );
      expect( formatNegative( '-1600.10' ) ).toBe( '&#8722;1600.10' );
    } );
  } );
} );
