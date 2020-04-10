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

  describe( 'makeScale', () => {
    it( 'creates an evenly-spaced scale for a exponential dataset', () => {
      const data = [];
      for ( let i = 1; i <= 50; i++ ) {
        data.push( { displayValue: i * i } );
      }

      const actual = sut.makeScale( data, colors );
      expect( actual( 0 ) ).toEqual( '#ffffff' );
      expect( actual( 100 ) ).toEqual( colors[0] );
      expect( actual( 361 ) ).toEqual( colors[1] ); // 19^2
      expect( actual( 784 ) ).toEqual( colors[2] ); // 28^2
      expect( actual( 1225 ) ).toEqual( colors[3] ); // 35^2
      expect( actual( 1681 ) ).toEqual( colors[4] ); // 41^2
      expect( actual( 2500 ) ).toEqual( colors[5] );
    } );

    it( 'scales differently if there are few unique values', () => {
      const data = [];
      for ( let i = 0; i < 51; i++ ) {
        data.push( { displayValue: 0 } );
      }
      data[3].displayValue = 900;

      const actual = sut.makeScale( data, colors );
      expect( actual( 0 ) ).toEqual( '#ffffff' );
      expect( actual( 300 ) ).toEqual( colors[1] );
      expect( actual( 450 ) ).toEqual( colors[2] );
      expect( actual( 790 ) ).toEqual( colors[5] );
    } );
  } );

  it( 'navigates the url to all complaints when clicked', () => {
    window.location.assign = jest.fn();
    expect( window.location.href ).toEqual( 'http://localhost/' );
    const evt = {
      point: {
        name: 'TX'
      }
    };
    sut.clickHandler( false, evt );
    expect( window.location.assign ).toBeCalledWith( 'http://localhost/search/?dateInterval=3y&dataNormalization=None&state=TX' );
  } );

  it( 'navigates the url to per capita when clicked', () => {
    window.location.assign = jest.fn();
    expect( window.location.href ).toEqual( 'http://localhost/' );
    const evt = {
      point: {
        name: 'TX'
      }
    };
    sut.clickHandler( true, evt );
    expect( window.location.assign ).toBeCalledWith( 'http://localhost/search/?dateInterval=3y&dataNormalization=Per%201000%20pop.&state=TX' );
  } );

  it( 'formats a map tile', () => {
    sut.point = {
      displayValue: 10000,
      name: 'FA'
    };

    const result = sut.tileFormatter();
    expect( result )
      .toEqual( '<div class="highcharts-data-label-state tile-FA ">' +
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
      '<p class="u-float-left">Per 1000 population</p><p class="u-right">3.12</p>' +
      '</div><div class="row u-clearfix"><p class="u-float-left">' +
      'Product with highest complaint volume</p><p class="u-right">' +
      'Expensive Item</p></div><div class="row u-clearfix">' +
      '<p class="u-float-left">Issue with highest complaint volume</p>' +
      '<p class="u-right">Being Broke</p></div>' );
  } );

  it( 'Processes the map data', () => {
    const scale = jest.fn().mockReturnValue( 'rgba(247, 248, 249, 1)' );

    const result = sut.processMapData( complaints.raw, scale );
    // test only the first one just make sure that the path and color are found
    expect( result[0] ).toEqual( {
      className: 'default',
      name: 'AK',
      fullName: 'Alaska',
      value: 713,
      issue: 'Incorrect information on your report',
      product: 'Credit reporting, credit repair services, or other personal consumer reports',
      perCapita: 0.97,
      displayValue: 713,
      color: 'rgba(247, 248, 249, 1)',
      path: 'M92,-245L175,-245,175,-162,92,-162,92,-245'
    } );
    expect( result[1] ).toEqual( {
      className: 'deselected',
      name: 'AL',
      fullName: 'Alabama',
      value: 10380,
      issue: 'Incorrect information on your report',
      product: 'Credit reporting, credit repair services, or other personal consumer reports',
      perCapita: 2.14,
      displayValue: 10380,
      color: 'rgba(247, 248, 249, 1)',
      path: 'M550,-337L633,-337,633,-253,550,-253,550,-337'
    } );

    expect( result[2] ).toEqual( {
      className: 'selected',
      name: 'AR',
      fullName: 'Arkansas',
      value: 4402,
      issue: 'Incorrect information on your report',
      product: 'Credit reporting, credit repair services, or other personal consumer reports',
      perCapita: 1.48,
      displayValue: 4402,
      color: 'rgba(247, 248, 249, 1)',
      path: 'M367,-428L450,-428,450,-345,367,-345,367,-428'
    } );
    expect( scale ).toHaveBeenCalledTimes( 51 );
  } );

  describe( 'legend', () => {
    let chart;
    beforeEach( () => {
      chart = {
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
    } );

    afterEach( () => {
      jest.clearAllMocks();
    } );
    it( 'draws large legend', () => {
      chart.renderer = chartMock;
      chart.chartWidth = 1000;
      const addSpies = jest.spyOn( chart.renderer, 'add' );
      sut._drawLegend( chart );
      expect( addSpies ).toHaveBeenCalledTimes( 25 );
    } );
    it( 'draws small legend', () => {
      chart.renderer = chartMock;
      chart.chartWidth = 599;
      const addSpies = jest.spyOn( chart.renderer, 'add' );
      sut._drawLegend( chart );
      expect( addSpies ).toHaveBeenCalledTimes( 25 );
    } );
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
