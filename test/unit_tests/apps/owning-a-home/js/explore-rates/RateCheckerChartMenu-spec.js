const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/owning-a-home/';
const RateCheckerChartMenu = require(
  BASE_JS_PATH + 'js/explore-rates/RateCheckerChartMenu'
);

import Highcharts from 'highcharts';

const HTML_SNIPPET = `
  <section id="chart-section" class="chart">
    <div class="chart-menu">
      <button class="chart-menu_btn
                     cf-icon
                     cf-icon__after
                     cf-icon-down">
        Download chart
      </button>
      <ul class="chart-menu_options">
        <li data-export-type="0">PNG</li>
        <li data-export-type="1">SVG</li>
        <li data-export-type="2">JPEG</li>
        <li data-export-type="3">Print chart</li>
      </ul>
    </div>
  </section>
`;

describe( 'explore-rates/RateCheckerChartMenu', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;

    let highCharts = new Highcharts.Chart( {
      chart: { renderTo:  document.querySelector( '.chart' ) }
    } );

    //const chartMenu = new RateCheckerChartMenu( highCharts );
  } );

  describe( 'render()', () => {
    xit( 'should hide the RateCheckerChartMenu', () => {
      const chartMenu = document.querySelector( '.chart-menu' );
      expect( chartMenu.classList.contains( 'chart-menu__open' ) ).toBe( false );
    } );

    xit( 'should set the base element', () => {
      const chartMenu = document.querySelector( '.chart-menu' );
      expect( chartMenu.classList.contains( 'chart-menu__open' ) ).toBe( false );
    } );
  } );

  xit( 'should open when clicked, if closed', () => {
    const dataLoadedDom =
      document.querySelector( '#chart-section .data-enabled' );
    expect( dataLoadedDom.classList.contains( 'loading' ) ).toBe( true );
    expect( dataLoadedDom.classList.contains( 'loaded' ) ).toBe( false );
  } );

  xit( 'should close when clicked, if open', () => {
    const dataLoadedDom =
      document.querySelector( '#chart-section .data-enabled' );
    expect( dataLoadedDom.classList.contains( 'loading' ) ).toBe( false );
    expect( dataLoadedDom.classList.contains( 'loaded' ) ).toBe( true );
  } );

  xit( 'should export the appropriate chart type', () => {
    const chartDom = document.querySelector( '#chart' );
    const resultAlertDom = document.querySelector( '#chart-result-alert' );
    expect( chartDom.classList.contains( 'warning' ) ).toBe( true );
    expect( resultAlertDom.classList.contains( 'u-hidden' ) ).toBe( false );
  } );
} );
