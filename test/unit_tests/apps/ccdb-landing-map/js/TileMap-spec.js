import 'regenerator-runtime/runtime';
import * as complaints from '../../../mocks/complaints';
import * as sut from '../../../../../cfgov/unprocessed/apps/ccdb-landing-map/js/TileMap.js';
import Analytics from '../../../../../cfgov/unprocessed/js/modules/Analytics';
import {
  TileMap
} from '../../../../../cfgov/unprocessed/apps/ccdb-landing-map/js/TileMap';
import chartMock from '../../../mocks/chartMock';

jest.mock( '../../../../../cfgov/unprocessed/js/modules/Analytics' );

/**
 * Create a mock for the window.location object, for testing purposes.
 */
function mockWindowLocation() {
  delete window.location;
  window.location = {
    protocol: 'http:',
    host: 'localhost',
    pathname: '/',
    href: 'http://localhost/',
    assign: jest.fn()
  };
}

describe( 'Tile map', () => {
  const colors = [
    'rgba(247, 248, 249, 0.5)',
    'rgba(212, 231, 230, 0.5)',
    'rgba(180, 210, 209, 0.5)',
    'rgba(137, 182, 181, 0.5)',
    'rgba(86, 149, 148, 0.5)',
    'rgba(37, 116, 115, 0.5)'
  ];

  let origMaxDate;
  beforeAll( () => {
    origMaxDate = global.MAX_DATE;
  } );

  // shim this so highcharts test doesn't die
  beforeEach( () => {
    delete global.MAX_DATE;
    delete global.complaint_public_metadata;
    window.SVGElement.prototype.getBBox = () => ( {
      x: 0,
      y: 0
      // whatever other props you need
    } );
  } );

  afterEach( () => {
    delete window.SVGElement.prototype.getBBox;
  } );

  afterAll( () => {
    global.MAX_DATE = origMaxDate;
  } );

  describe( 'startOfToday', () => {
    it( 'handles MAX_DATE that is already set', () => {
      global.MAX_DATE = new Date( '2016-05-09 02:39:23' );
      const actual = sut.startOfToday();
      expect( actual.getFullYear() ).toEqual( 2016 );
      expect( actual.getMonth() ).toEqual( 4 );
      expect( actual.getDate() ).toEqual( 9 );
      expect( actual.getHours() ).toEqual( 2 );
      expect( actual.getMinutes() ).toEqual( 39 );
    } );

    it( 'sets MAX_DATE from the metadata', () => {
      /* eslint-disable camelcase */
      global.complaint_public_metadata = {
        metadata_timestamp: '2020-05-09 02:39:23',
        qas_timestamp: '2020-05-08 23:48:52',
        total_count: 2611545
      };
      /* eslint-enable camelcase */

      const actual = sut.startOfToday();
      expect( actual.getFullYear() ).toEqual( 2020 );
      expect( actual.getMonth() ).toEqual( 4 );
      expect( actual.getDate() ).toEqual( 9 );
      expect( actual.getHours() ).toEqual( 0 );
      expect( actual.getMinutes() ).toEqual( 0 );
    } );

    it( 'defaults MAX_DATE if the metadata is missing', () => {
      jest.spyOn( global.Date, 'now' )
        // eslint-disable-next-line no-unused-vars
        .mockImplementationOnce( _ => Date.UTC( 2018, 4, 1, 4 ) );

      const actual = sut.startOfToday();
      expect( actual.getFullYear() ).toEqual( 2018 );
      expect( actual.getMonth() ).toEqual( 4 );
      expect( actual.getDate() ).toEqual( 1 );
      expect( actual.getHours() ).toEqual( 0 );
      expect( actual.getMinutes() ).toEqual( 0 );
    } );
  } );

  it( 'Calculates date range', () => {
    // set the date so result is always the same in the test
    const DATE_TO_USE = new Date( 'December 31, 2015 20:00:00' );
    global.Date = jest.fn( () => DATE_TO_USE );
    const result = sut.calculateDateRange();
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
      // 19^2
      expect( actual( 361 ) ).toEqual( colors[1] );
      // 28^2
      expect( actual( 784 ) ).toEqual( colors[2] );
      // 35^2
      expect( actual( 1225 ) ).toEqual( colors[3] );
      // 41^2
      expect( actual( 1681 ) ).toEqual( colors[4] );
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
    mockWindowLocation();

    expect( window.location.href ).toEqual( 'http://localhost/' );
    Analytics.getDataLayerOptions = jest.fn();
    Analytics.sendEvent = jest.fn();
    const evt = {
      point: {
        name: 'TX'
      }
    };
    sut.clickHandler( false, evt );
    expect( Analytics.getDataLayerOptions )
      .toHaveBeenCalledWith( 'State Event: click', 'TX', 'Consumer Complaint Search' );
    expect( Analytics.sendEvent ).toHaveBeenCalled();
    expect( window.location.assign ).toBeCalledWith( 'http://localhost/search/?dateRange=3y&dataNormalization=None&state=TX' );
  } );

  it( 'navigates the url to per capita when clicked', () => {
    mockWindowLocation();

    expect( window.location.href ).toEqual( 'http://localhost/' );
    const evt = {
      point: {
        name: 'TX'
      }
    };
    sut.clickHandler( true, evt );
    expect( window.location.assign ).toBeCalledWith( 'http://localhost/search/?dateRange=3y&dataNormalization=Per%201000%20pop.&state=TX' );
  } );

  it( 'formats a map tile', () => {
    sut.point = {
      displayValue: 10000,
      name: 'FA'
    };

    const result = sut.tileFormatter();
    expect( result )
      .toEqual( '<div class="highcharts-data-label-state tile-FA ">' +
      '<span class="abbr">FA</span>' +
      '<span class="value">10,000</span></div>' );
  } );

  it( 'formats a map tile in Internet Explorer', () => {
    sut.point = {
      className: 'selected',
      displayValue: 10000,
      name: 'FA'
    };

    Object.defineProperty(
      window.navigator,
      'userAgent',
      { value: 'MSIE' }
    );

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

  it( 'shortens long numbers', () => {
    const cases = [
      { n: 0, val: '0' },
      { n: 7, val: '7' },
      { n: 42, val: '42' },
      { n: 567, val: '567' },
      { n: 3456, val: '3.4K' },
      { n: 9873, val: '9.8K' },
      { n: 23456, val: '23K' },
      { n: 98765, val: '98K' },
      { n: 234567, val: '234K' },
      { n: 782345, val: '782K' },
      { n: 1450000, val: '1.4M' },
      { n: 9870000, val: '9.8M' }
    ];

    cases.forEach( x => {
      expect( sut.makeShortName( x.n ) ).toEqual( x.val );
    } );
  } );

  it( 'formats a series point for voice-over reading', () => {
    const point = {
      fullName: 'Foo',
      displayValue: '13'
    };
    const actual = sut.pointDescriptionFormatter( point );
    expect( actual ).toEqual( 'Foo 13' );
  } );


  describe( 'generating bins', () => {
    let scaleFn;
    beforeEach( () => {
      scaleFn = jest.fn( x => x );
    } );

    it( 'gets complaints bins - All', () => {
      const quantiles = [
        880.2857142857142,
        1622.5714285714282,
        3064.9999999999995,
        6136.714285714284,
        7788.142857142858,
        13909.714285714286
      ];
      const expected = [
        { from: 0, color: '#ffffff', name: '≥ 0', shortName: '≥ 0' },
        { from: 880, color: 881, name: '> 880', shortName: '> 880' },
        { from: 1623, color: 1623, name: '≥ 1,623', shortName: '≥ 1.6K' },
        { from: 3065, color: 3065, name: '≥ 3,065', shortName: '≥ 3.0K' },
        { from: 6137, color: 6137, name: '≥ 6,137', shortName: '≥ 6.1K' },
        { from: 7788, color: 7789, name: '> 7,788', shortName: '> 7.7K' },
        { from: 13910, color: 13910, name: '≥ 13,910', shortName: '≥ 13K' }
      ];

      const result = sut.getBins( quantiles, scaleFn );
      expect( result ).toEqual( expected );
    } );

    it( 'gets complaints bins - one zip code', () => {
      const quantiles = [
        0.2857142857142857,
        0.5714285714285714,
        0.8571428571428571,
        183.99999999999991,
        550,
        915.9999999999999
      ];
      const expected = [
        { from: 0, color: '#ffffff', name: '≥ 0', shortName: '≥ 0' },
        { from: 1, color: 1, name: '≥ 1', shortName: '≥ 1' },
        { from: 184, color: 184, name: '≥ 184', shortName: '≥ 184' },
        { from: 550, color: 550, name: '≥ 550', shortName: '≥ 550' },
        { from: 916, color: 916, name: '≥ 916', shortName: '≥ 916' }
      ];

      const result = sut.getBins( quantiles, scaleFn );
      expect( result ).toEqual( expected );
    } );

    it( 'gets complaints bins - max 2 complaints', () => {
      const quantiles = [
        0.2857142857142857,
        0.5714285714285714,
        0.8571428571428571,
        1.1428571428571428,
        1.4285714285714286,
        1.7142857142857142
      ];
      const expected = [
        { from: 0, color: '#ffffff', name: '≥ 0', shortName: '≥ 0' },
        { from: 1, color: 1, name: '≥ 1', shortName: '≥ 1' },
        { from: 2, color: 2, name: '≥ 2', shortName: '≥ 2' }
      ];

      const result = sut.getBins( quantiles, scaleFn );
      expect( result ).toEqual( expected );
    } );

    it( 'gets complaints bins - max 1 complaint', () => {
      const quantiles = [
        0.14285714285714285,
        0.2857142857142857,
        0.42857142857142855,
        0.5714285714285714,
        0.7142857142857143,
        0.8571428571428571
      ];
      const expected = [
        { from: 0, color: '#ffffff', name: '≥ 0', shortName: '≥ 0' },
        { from: 1, color: 1, name: '≥ 1', shortName: '≥ 1' }
      ];

      const result = sut.getBins( quantiles, scaleFn );
      expect( result ).toEqual( expected );
    } );

    it( 'gets Per 1000 population bins', () => {
      const quantiles = [
        1.1928571428571428,
        1.4657142857142857,
        1.81,
        2.0357142857142856,
        2.33,
        2.845714285714285
      ];
      const expected = [
        { from: 0, color: '#ffffff', name: '≥ 0', shortName: '≥ 0' },
        { from: 1.19, color: quantiles[0], name: '> 1.19', shortName: '> 1.19' },
        { from: 1.46, color: quantiles[1], name: '> 1.46', shortName: '> 1.46' },
        { from: 1.81, color: quantiles[2], name: '≥ 1.81', shortName: '≥ 1.81' },
        { from: 2.03, color: quantiles[3], name: '> 2.03', shortName: '> 2.03' },
        { from: 2.33, color: quantiles[4], name: '≥ 2.33', shortName: '≥ 2.33' },
        { from: 2.84, color: quantiles[5], name: '> 2.84', shortName: '> 2.84' }
      ];

      const result = sut.getPerCapitaBins( quantiles, scaleFn );
      expect( result ).toEqual( expected );
    } );
  } );

  it( 'handles no values for colors', () => {
    const color = sut.getColorByValue( null, null );
    expect( color ).toEqual( '#ffffff' );
  } );
} );
