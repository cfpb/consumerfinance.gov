const BASE_JS_PATH = '../../../../../unprocessed/js/';
const arrayHelpers = require( BASE_JS_PATH + 'modules/util/array-helpers' );
let array;
let index;

describe( 'array-helpers', () => {

  describe( 'indexOfObject()', () => {

    it( 'should return -1 if the array is empty', () => {
      array = [];
      index = arrayHelpers.indexOfObject( array, 'foo' );

      expect( index ).toBe( -1 );
    } );

    it( 'should return -1 if there is no match', () => {
      array = [
        { value: 'bar' },
        { value: 'baz' }
      ];
      index = arrayHelpers.indexOfObject( array, 'value', 'foo' );

      expect( index ).toBe( -1 );
    } );

    it( 'should return the matched index', () => {
      array = [
        { value: 'foo' },
        { value: 'bar' },
        { value: 'baz' }
      ];
      index = arrayHelpers.indexOfObject( array, 'value', 'foo' );

      expect( index ).toBe( 0 );
    } );
  } );

  describe( 'uniquePrimitives()', () => {
    it( 'should return an array without duplicate primitives', () => {
      const testArray = [ 1, 2, 2, 3, 3, 3, '4.500%', '4.500%', null, null ];
      const testArrayMatch = [ 1, 2, 3, '4.500%', null ];

      const newArr = arrayHelpers.uniquePrimitives( testArray );

      expect( newArr ).toStrictEqual( testArrayMatch );
    } );
  } );
} );
