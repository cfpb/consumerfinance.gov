import * as complaints from '../../../mocks/complaints';
import * as sut from '../../../../../cfgov/unprocessed/apps/ccdb-landing-map/js/TileMap.js';
import TileMap from '../../../../../cfgov/unprocessed/apps/ccdb-landing-map/js/TileMap';
import chartMock from '../../../mocks/chartMock';

describe( 'Tile map', () => {
  const colors = [
    'rgba(247, 248, 249, 0.5)',
    'rgba(212, 231, 230, 0.5)',
    'rgba(180, 210, 209, 0.5)',
    'rgba(137, 182, 181, 0.5)',
    'rgba(86, 149, 148, 0.5)',
    'rgba(37, 116, 115, 0.5)'
  ];

  // shim this so highcharts test doesn't die
  beforeEach( () => {
    window.SVGElement.prototype.getBBox = () => ( {
      x: 0,
      y: 0
      // whatever other props you need
    } );
  } );

  afterEach( () => {
    delete window.SVGElement.prototype.getBBox;
  } );

  it( 'Calculates date interval', () => {
    // set the date so result is always the same in the test
    const DATE_TO_USE = new Date( '2016' );
    global.Date = jest.fn( () => DATE_TO_USE );
    const result = sut.calculateDateInterval();
    expect( result ).toContain( '12/31/2012 - 12/31/2015' );
  } );

  it( 'Finds Max Complaints', () => {
    const state = { displayValue: 1000, name: 'Foo' };
    const result = sut.findMaxComplaints( 50, state );
    expect( result ).toEqual( 1000 );
  } );

  it( 'gets empty raw  bins', () => {
    const result = sut.getBins( [], colors );
    expect( result ).toEqual( [] );
  } );

  it( 'gets Raw Complaints bins', () => {
    const result = sut.getBins( complaints.raw, colors );
    expect( result )
      .toEqual( [
        {
          color: 'rgba(247, 248, 249, 0.5)',
          from: 1,
          name: '≥ 0',
          to: 16435
        },
        {
          color: 'rgba(212, 231, 230, 0.5)',
          from: 16435,
          name: '≥ 16K',
          to: 32868
        },
        {
          color: 'rgba(180, 210, 209, 0.5)',
          from: 32868,
          name: '≥ 33K',
          to: 49302
        },
        {
          color: 'rgba(137, 182, 181, 0.5)',
          from: 49302,
          name: '≥ 49K',
          to: 65735
        },
        {
          color: 'rgba(86, 149, 148, 0.5)',
          from: 65735,
          name: '≥ 66K',
          to: 82169
        },
        {
          color: 'rgba(37, 116, 115, 0.5)',
          from: 82169,
          name: '≥ 82K',
          // eslint-disable-next-line no-undefined
          to: undefined
        } ] );
  } );

  it( 'gets empty per capita bins', () => {
    const result = sut.getPerCapitaBins( [], colors );
    expect( result ).toEqual( [] );
  } );

  it( 'gets Per Capita bins', () => {
    const result = sut.getPerCapitaBins( complaints.perCapita, colors );
    expect( result )
      .toEqual( [
        { color: '#fff', from: 0, name: '>0', to: 0.7516666666666666 },
        {
          color: 'rgba(247, 248, 249, 0.5)',
          from: 1,
          name: '≥ 1',
          to: 1.75
        },
        {
          color: 'rgba(212, 231, 230, 0.5)',
          from: 1.75,
          name: '≥ 1.75',
          to: 2.5
        },
        {
          color: 'rgba(180, 210, 209, 0.5)',
          from: 2.5,
          name: '≥ 2.5',
          to: 3.25
        },
        {
          color: 'rgba(137, 182, 181, 0.5)',
          from: 3.25,
          name: '≥ 3.25',
          to: 4
        },
        {
          color: 'rgba(86, 149, 148, 0.5)',
          from: 4,
          name: '≥ 4',
          // eslint-disable-next-line no-undefined
          to: undefined
        },
        {
          color: 'rgba(37, 116, 115, 0.5)',
          from: 4.75,
          name: '≥ 4.75',
          to: 5.5
        } ] );
  } );

  it( 'Gets color of a tile based on bin limits', () => {
    const bins = [
      { color: 'white', from: 0 },
      { color: 'green', from: 10 },
      { color: 'red', from: 30 }
    ];
    let result = sut.getColorByValue( 23, bins );
    expect( result ).toEqual( 'green' );
    result = sut.getColorByValue( null, bins );
    expect( result ).toEqual( '#ffffff' );
  } );

  it( 'formats a map tile', () => {
    sut.point = {
      displayValue: 10000,
      name: 'FA'
    };

    const result = sut.tileFormatter();
    expect( result )
      .toEqual( '<div class="highcharts-data-label-state">' +
      '<span class="abbr">FA</span><br />' +
      '<span class="value">10,000</span></div>' );
  } );

  it( 'formats the map tooltip w/ missing data', () => {
    sut.fullName = 'Another Name';
    sut.value = 10000;
    const result = sut.tooltipFormatter();
    expect( result ).toEqual( '<div class="title">Another Name' +
      '</div><div class="row u-clearfix"><p class="u-float-left">Complaints' +
      '</p><p class="u-right">10,000</p></div>' );
  } );

  it( 'formats the map tooltip w/ prod & issue', () => {
    sut.fullName = 'State Name';
    sut.value = 10000;
    sut.perCapita = 3.12;
    sut.product = 'Expensive Item';
    sut.issue = 'Being Broke';
    const result = sut.tooltipFormatter();
    expect( result ).toEqual( '<div class="title">State Name' +
      '</div><div class="row u-clearfix"><p class="u-float-left">Complaints' +
      '</p><p class="u-right">10,000</p></div><div class="row u-clearfix">' +
      '<p class="u-float-left">Per capita</p><p class="u-right">3.12</p>' +
      '</div><div class="row u-clearfix"><p class="u-float-left">' +
      'Product with highest complaint volume</p><p class="u-right">' +
      'Expensive Item</p></div><div class="row u-clearfix">' +
      '<p class="u-float-left">Issue with highest complaint volume</p>' +
      '<p class="u-right">Being Broke</p></div>' );
  } );

  it( 'Processes the map data', () => {
    const bins = [
      {
        color: 'rgba(247, 248, 249, 0.5)',
        from: 1,
        name: '≥ 0',
        to: 16435
      },
      {
        color: 'rgba(212, 231, 230, 0.5)',
        from: 16435,
        name: '≥ 16K',
        to: 32868
      },
      {
        color: 'rgba(180, 210, 209, 0.5)',
        from: 32868,
        name: '≥ 33K',
        to: 49302
      },
      {
        color: 'rgba(137, 182, 181, 0.5)',
        from: 49302,
        name: '≥ 49K',
        to: 65735
      },
      {
        color: 'rgba(86, 149, 148, 0.5)',
        from: 65735,
        name: '≥ 66K',
        to: 82169
      },
      {
        color: 'rgba(37, 116, 115, 0.5)',
        from: 82169,
        name: '≥ 82K',
        // eslint-disable-next-line no-undefined
        to: undefined
      } ];
    const result = sut.processMapData( complaints.raw, bins );
    // test only the first one just make sure that the path and color are found
    expect( result[0] ).toEqual( {
      name: 'AK',
      fullName: 'Alaska',
      value: 713,
      issue: 'Incorrect information on your report',
      product: 'Credit reporting, credit repair services, or other personal consumer reports',
      perCapita: 0.97,
      displayValue: 713,
      color: 'rgba(247, 248, 249, 0.5)',
      path: 'M92,-245L175,-245,175,-162,92,-162,92,-245'
    } );
  } );

  it( 'draws the legend', () => {
    const chart = {
      options: {
        bins: [
          {
            color: 'rgba(247, 248, 249, 0.5)',
            from: 1,
            name: '≥ 0',
            to: 16435
          },
          {
            color: 'rgba(212, 231, 230, 0.5)',
            from: 16435,
            name: '≥ 16K',
            to: 32868
          },
          {
            color: 'rgba(180, 210, 209, 0.5)',
            from: 32868,
            name: '≥ 33K',
            to: 49302
          },
          {
            color: 'rgba(137, 182, 181, 0.5)',
            from: 49302,
            name: '≥ 49K',
            to: 65735
          },
          {
            color: 'rgba(86, 149, 148, 0.5)',
            from: 65735,
            name: '≥ 66K',
            to: 82169
          },
          {
            color: 'rgba(37, 116, 115, 0.5)',
            from: 82169,
            name: '≥ 82K',
            // eslint-disable-next-line no-undefined
            to: undefined
          } ],
        legend: {
          legendTitle: 'Foo'
        }
      },
      margin: []

    };

    chart.renderer = chartMock;
    const addSpies = jest.spyOn( chart.renderer, 'add' );
    sut._drawLegend( chart );
    expect( addSpies ).toHaveBeenCalledTimes( 25 );
  } );

  it( 'can construct a map', () => {
    const options = {
      el: document.createElement( 'div' ),
      data: [],
      isPerCapita: false
    };

    const drawSpy = jest.spyOn( TileMap.prototype, 'draw' );
    // eslint-disable-next-line no-unused-vars
    const map = new TileMap( options );
    expect( drawSpy ).toHaveBeenCalled();
  } );

  it( 'can construct a perCapita map', () => {
    const options = {
      el: document.createElement( 'div' ),
      data: [],
      isPerCapita: true
    };

    const drawSpy = jest.spyOn( TileMap.prototype, 'draw' );
    // eslint-disable-next-line no-unused-vars
    const map = new TileMap( options );

    expect( drawSpy ).toHaveBeenCalled();
  } );
} );
