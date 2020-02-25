import * as sut from '../../../../../cfgov/unprocessed/apps/ccdb-landing-map/js/TileMap.js';

describe( 'Tile map', () => {

  it('Calculates date interval', ()=>{
    // set the date so result is always the same in the test
    const DATE_TO_USE = new Date('2016');
    global.Date = jest.fn(() => DATE_TO_USE);
    const intervalText = sut.calculateDateInterval();
    expect(intervalText).toContain('12/31/2012 - 12/31/2015');
  });

  it('Finds Max Complaints', ()=>{
    const state = { displayValue: 1000, name: 'Foo'}
    const intervalText = sut.findMaxComplaints(50, state);
    expect(intervalText).toEqual(1000);
  });
  // it('does stuff', ()=>{
  //   const intervalText = sut.getBins([], null);
  //   expect(intervalText).toContain(' - ');
  // });
  // it('does stuff', ()=>{
  //   const intervalText = sut.getColorByValue('234');
  //   expect(intervalText).toContain(' - ');
  // });
  //
  // it('does stuff', ()=>{
  //   const intervalText = sut.getPerCapitaBins('234');
  //   expect(intervalText).toContain(' - ');
  // });
  //
  // it('does stuff', ()=>{
  //   const intervalText = sut.processMapData('234');
  //   expect(intervalText).toContain(' - ');
  // });
  //
  // it('does stuff', ()=>{
  //   const intervalText = sut.tileFormatter();
  //   expect(intervalText).toContain(' - ');
  // });
  //
  // it('does stuff', ()=>{
  //   const intervalText = sut.tooltipFormatter();
  //   expect(intervalText).toContain(' - ');
  // });
} );
