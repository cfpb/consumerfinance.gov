const sampleTest = require(
  '../../../../cfgov/unprocessed/js/modules/sample-test.js'
);

describe( 'sample test javascript file', () => {

  it.skip( 'should return a string', () => {
    expect( sampleTest.init() ).toBe( 'Shredder' );
  } );

} );
