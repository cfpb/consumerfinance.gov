import {
  JS_HOOK,
<<<<<<< HEAD
  noopFunct
=======
  noopFunct,
  UNDEFINED
>>>>>>> Convert JS to use ES6 modules
} from '../../../../../cfgov/unprocessed/js/modules/util/standard-type';

describe( 'standard-type', () => {
  it( 'should include a standard JS data hook', () => {
    expect( JS_HOOK ).toBe( 'data-js-hook' );
  } );

  it( 'should include a non operational function', () => {
    expect( noopFunct() ).toBeUndefined();
<<<<<<< HEAD
=======
  } );

  it( 'should include a standard undefined reference', () => {
    expect( UNDEFINED ).toBeUndefined();
>>>>>>> Convert JS to use ES6 modules
  } );
} );
