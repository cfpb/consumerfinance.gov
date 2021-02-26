import 'regenerator-runtime/runtime';
import
* as d3
  from '../../../../../cfgov/unprocessed/apps/ccdb-landing-map/node_modules/d3-selection';
import
* as sut
  from '../../../../../cfgov/unprocessed/apps/ccdb-landing-map/js/TileMap.js';

describe( 'Tile map: mouse events', () => {
  it( 'can mouseOut tiles', () => {
    sut.name = 'fooout';
    const d3Spy = jest.spyOn( d3, 'select' );
    sut.mouseoutPoint();
    expect( d3Spy ).toHaveBeenCalledWith( '.tile-fooout' );
  } );

  it( 'can mouseOver tiles', () => {
    sut.name = 'fooover';
    const d3Spy = jest.spyOn( d3, 'select' );
    sut.mouseoverPoint();
    expect( d3Spy ).toHaveBeenCalledWith( '.tile-fooover' );
  } );

} );
