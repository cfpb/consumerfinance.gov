import {
  toArray
} from '../../../../../../../cfgov/unprocessed/js/routes/on-demand/youth-employment-programs/buying-a-car/util.js';

describe( 'YEP utility functions', () => {

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
      const children = [
        document.createElement( 'a' ),
        document.createElement( 'a' )
      ];
      children.forEach( child => fragment.appendChild( child ) );

      const dom = document.createElement( 'div' );
      dom.appendChild( fragment );
      const array = toArray( dom.querySelectorAll( 'a' ) );

      expect( array.slice ).toBeDefined();
    } );
  } );
} );
