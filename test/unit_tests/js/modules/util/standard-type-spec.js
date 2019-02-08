import {
  JS_HOOK,
  noopFunct
} from '../../../../../cfgov/unprocessed/js/modules/util/standard-type';

describe( 'standard-type', () => {
  it( 'should include a standard JS data hook', () => {
    expect( JS_HOOK ).toBe( 'data-js-hook' );
  } );

  it( 'should include a non operational function', () => {
    expect( noopFunct() ).toBeUndefined();
  } );
} );
