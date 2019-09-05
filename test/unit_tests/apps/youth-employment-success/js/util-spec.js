import {
  actionCreator,
  assign,
  entries
} from '../../../../../cfgov/unprocessed/apps/youth-employment-success/js/util';

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
      expect( assign( originalObject, override ).agency ).toBe( override.agency );
    } );

    it( 'does not mutate the original object', () => {
      expect( assign( originalObject ) ).not.toBe( originalObject );
    } );
  } );

  describe( '.entries', () => {
    it( 'throws an error when it receives a value that isn\'t an object', () => {
      const invalidArgs = [ function() { return 'a'; }, null, 1, 'bad', [] ];

      invalidArgs.forEach( invalidArg => expect( () => entries( invalidArg ) ).toThrow()
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
} );
