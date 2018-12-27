const sample = require(
  '../../../../cfgov/unprocessed/js/modules/sample.js'
);

describe( 'sample', () => {

  it.skip( 'should return a string', () => {
    expect( sample.init() ).toBe( 'Shredder' );
  } );

} );
