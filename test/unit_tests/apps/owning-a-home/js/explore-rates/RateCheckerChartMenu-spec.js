const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/owning-a-home/';
const RateCheckerChartMenu = require(
  BASE_JS_PATH + 'js/explore-rates/RateCheckerChartMenu'
).default;

const Highcharts = require(
  BASE_JS_PATH + 'node_modules/highcharts'
);

import { simulateEvent } from '../../../../../util/simulate-event';

const STATE_OPEN = 'open';
const STATE_CLOSED = 'closed';

let highCharts;
let chartMenu;
let chartMenuDOM;
let chartMenuBtnDOM;

const HTML_SNIPPET = `
<section id="chart-section" class="chart">
  <div class="chart-menu">
    <button class="chart-menu_btn
                    cf-icon
                    cf-icon__after
                    cf-icon-download">
      Download chart
    </button>
    <ul class="chart-menu_options">
      <li>PNG</li>
      <li>SVG</li>
      <li>JPEG</li>
      <li>Print chart</li>
    </ul>
  </div>
  <figure>
    <div id="chart" class="chart-area"></div>
  </figure>
</section>
`;

describe( 'explore-rates/RateCheckerChartMenu', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;

    highCharts = new Highcharts.Chart( {
      chart: {
        renderTo: document.querySelector( '#chart' )
      },
      xAxis: {
        categories: [ 'Jan', 'Feb' ]
      },
      series: [ {
        data: [ 29.9, 71.5 ]
      } ]
    } );

    highCharts.exportChart = jest.fn();
    highCharts.print = jest.fn();

    chartMenu = new RateCheckerChartMenu( highCharts );
    chartMenuDOM = document.querySelector( '.chart-menu' );
    chartMenuBtnDOM = document.querySelector( '.chart-menu_btn' );
  } );

  describe( 'new RateCheckerChartMenu()', () => {
    it( 'should set the state to closed', () => {
      expect( chartMenu.state ).toStrictEqual( STATE_CLOSED );
    } );

    it( 'should set a reference to the highcharts instance', () => {
      expect( highCharts ).toStrictEqual( chartMenu.highCharts );
    } );

    it( 'should set a reference to the base element', () => {
      expect( chartMenuDOM.isEqualNode( chartMenu.element ) ).toBe( true );
    } );

    it( 'should initialize the click event on the menu element', () => {
      const _initEvents = RateCheckerChartMenu.prototype._initEvents;
      const mockInitEvents = jest.fn();
      RateCheckerChartMenu.prototype._initEvents = mockInitEvents;
      chartMenu = new RateCheckerChartMenu( highCharts );

      expect( mockInitEvents.mock.calls.length ).toBe( 1 );
      RateCheckerChartMenu.prototype._initEvents = _initEvents;
    } );
  } );

  describe( 'open()', () => {
    it( 'should set the open state', () => {
      chartMenu.open();
      expect( chartMenu.state ).toStrictEqual( STATE_OPEN );
    } );
  } );

  describe( 'close()', () => {
    it( 'should set the closed state', () => {
      chartMenu.close();
      expect( chartMenu.state ).toStrictEqual( STATE_CLOSED );
    } );
  } );

  describe( 'render()', () => {
    it( 'should set the proper classes on the menu DOM', () => {
      chartMenu.open();
      expect( chartMenu.state ).toStrictEqual( STATE_OPEN );
      expect( chartMenuDOM.classList.contains( 'chart-menu__open' ) )
        .toStrictEqual( true );
    } );
  } );

  describe( 'onClick()', () => {
    it( 'should set the proper classes when the menu button is clicked', () => {
      simulateEvent( 'click', chartMenuBtnDOM );
      expect( chartMenuDOM.classList.contains( 'chart-menu__open' ) )
        .toStrictEqual( true );
      simulateEvent( 'click', chartMenuBtnDOM );
      expect( chartMenuDOM.classList.contains( 'chart-menu__open' ) )
        .toStrictEqual( false );
    } );

    it( 'should set the proper state when the menu button is clicked', () => {
      simulateEvent( 'click', chartMenuBtnDOM );
      expect( chartMenu.state ).toStrictEqual( STATE_OPEN );
      simulateEvent( 'click', chartMenuBtnDOM );
      expect( chartMenu.state ).toStrictEqual( STATE_CLOSED );
    } );

    it( 'should call exportChart when a menu export option is clicked', () => {
      const spy = jest.spyOn( chartMenu, 'exportChart' );
      simulateEvent( 'click', chartMenuBtnDOM );
      simulateEvent( 'click', chartMenuDOM.querySelector( 'li' ) );
      expect( spy ).toHaveBeenCalled();
      spy.mockReset();
      spy.mockRestore();
    } );
  } );

  describe( 'exportChart()', () => {
    it( 'should call the appropriate highCharts.export method', () => {
      chartMenu.exportChart( 'PNG' );
      expect( highCharts.exportChart ).toBeCalledWith( { type: 'image/png' } );
      chartMenu.exportChart( 'SVG' );
      expect( highCharts.exportChart ).toBeCalledWith( { type: 'image/svg+xml' } );
      chartMenu.exportChart( 'JPEG' );
      expect( highCharts.exportChart ).toBeCalledWith( { type: 'image/jpeg' } );
      chartMenu.exportChart( 'Print chart' );
      expect( highCharts.print ).toHaveBeenCalled();
    } );
  } );
} );
