const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/owning-a-home/';
const RateCheckerChartMenu = require(
  BASE_JS_PATH + 'js/explore-rates/RateCheckerChartMenu'
).default;

const Highcharts = require(
  BASE_JS_PATH + 'node_modules/highcharts'
);

const simulateEvent =
  require( '../../../../../util/simulate-event' ).simulateEvent;

const STATES = RateCheckerChartMenu.STATES;

let highCharts;
let chartMenu;
let chartMenuDOM;
let chartMenuBtnDOM;

const HTML_SNIPPET = `
  <section id="chart-section" class="chart">
  </section>
    <div class="chart-menu">
      <button class="chart-menu_btn
                     cf-icon
                     cf-icon__after
                     cf-icon-download">
        Download chart
      </button>
      <ul class="chart-menu_options">
        <li data-export-type="0">PNG</li>
        <li data-export-type="1">SVG</li>
        <li data-export-type="2">JPEG</li>
        <li data-export-type="3">Print chart</li>
      </ul>
    </div>
`;

describe( 'explore-rates/RateCheckerChartMenu', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;

    highCharts = new Highcharts.Chart( 'chart-section', {
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
      expect( chartMenu.state ).toEqual( { position: STATES.CLOSED } );
    } );

    it( 'should set a reference to the highcharts instance', () => {
      expect( highCharts ).toEqual( chartMenu.highCharts );
    } );

    it( 'should set a reference to the base element', () => {
      expect( chartMenuDOM.isEqualNode( chartMenu.element ) ).toBe( true );
    } );

    it( 'should initialize the click event on the menu element', () => {
      const _initEvents = RateCheckerChartMenu.prototype._initEvents;
      const mockInitEvents = jest.fn();
      RateCheckerChartMenu.prototype._initEvents = mockInitEvents;
      const chartMenu = new RateCheckerChartMenu( highCharts );

      expect( mockInitEvents.mock.calls.length ).toBe( 1 );
      RateCheckerChartMenu.prototype._initEvents = _initEvents;
    } );
  } );

  describe( 'open()', () => {
    it( 'should set the open state', () => {
      chartMenu.open();
      expect( chartMenu.state ).toEqual( { position: STATES.OPEN } );
    } );
  } );

  describe( 'close()', () => {
    it( 'should set the closed state', () => {
      chartMenu.close();
      expect( chartMenu.state ).toEqual( { position: STATES.CLOSED } );
    } );
  } );

  describe( 'render()', () => {
    it( 'should set the proper classes on the menu DOM', () => {
      chartMenu.open();
      expect( chartMenuDOM.classList.contains( 'chart-menu__open' ) )
        .toEqual( true );
    } );
  } );

  describe( '_setState()', () => {
    it( 'should set the state when passed an object', () => {
      chartMenu._setState( { position: STATES.OPEN } );
      expect( chartMenu.state ).toEqual( { position: STATES.OPEN } );
    } );

    it( 'should maintain the state when an object isn\'t passed', () => {
      chartMenu.open();
      expect( chartMenu.state ).toEqual( { position: STATES.OPEN } );
      chartMenu._setState();
      expect( chartMenu.state ).toEqual( { position: STATES.OPEN } );
    } );
  } );

  describe( 'onClick()', () => {
    it( 'should set the proper classes when the menu button is clicked', () => {
      simulateEvent( 'click', chartMenuBtnDOM );
      expect( chartMenuDOM.classList.contains( 'chart-menu__open' ) )
        .toEqual( true );
      simulateEvent( 'click', chartMenuBtnDOM );
      expect( chartMenuDOM.classList.contains( 'chart-menu__open' ) )
        .toEqual( false );
    } );

    it( 'should set the proper state when the menu button is clicked', () => {
      simulateEvent( 'click', chartMenuBtnDOM );
      expect( chartMenu.state ).toEqual( { position: STATES.OPEN } );
      simulateEvent( 'click', chartMenuBtnDOM );
      expect( chartMenu.state ).toEqual( { position: STATES.CLOSED } );
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
      chartMenu.exportChart( 1 );
      expect( highCharts.exportChart ).toBeCalledWith( { type: 'image/svg+xml' } );
      chartMenu.exportChart( 2 );
      expect( highCharts.exportChart ).toBeCalledWith( { type: 'image/jpeg' } );
      chartMenu.exportChart( 3 );
      expect( highCharts.print ).toHaveBeenCalled();
    } );
  } );
} );
