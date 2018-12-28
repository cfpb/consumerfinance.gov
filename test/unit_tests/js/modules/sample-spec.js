import * as sample from '../../../../cfgov/unprocessed/js/modules/sample.js';
let sampleString;

describe( 'sample', () => {

  it.skip( 'should return a string with expected value', () => {
    sampleString = 'Shredder';
    expect( sample.init() ).toBe( sampleString );
  } );

} );
