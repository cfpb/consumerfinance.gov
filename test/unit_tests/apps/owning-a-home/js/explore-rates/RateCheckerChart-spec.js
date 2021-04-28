import {
  RateCheckerChart
} from '../../../../../../cfgov/unprocessed/apps/owning-a-home/js/explore-rates/RateCheckerChart';

const HTML_SNIPPET = `
<section id="chart-section" class="chart">

  <figure class="data-enabled loading">
      <div id="chart" class="chart-area"></div>
      <figcaption class="chart-caption">
          <div class="caption-title">
              Interest rates for your situation
          </div>
          <div class="rc-data-link">
              <a href="#about" class="u-link-underline">
                  About our data source
              </a>
          </div>
      </figcaption>
  </figure>

  <div id="chart-result-alert"
       class="result-alert chart-alert u-hidden"
       role="alert">
  </div>

  <div id="chart-fail-alert"
       class="result-alert chart-alert u-hidden"
       role="alert">
  </div>

</section>
`;

let chart;

describe( 'explore-rates/RateCheckerChart', () => {
  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    chart = new RateCheckerChart();
    chart.init();
  } );

  describe( 'render()', () => {
    it( 'should add geolocating class', () => {
      chart.render();
      const containerDom = document.querySelector( '#chart-section' );
      expect( containerDom.classList.contains( 'geolocating' ) ).toBe( true );
    } );

    it( 'should remove geolocating class', () => {
      const mockData = { labels: {}, vals: {}};
      chart.render();
      chart.render( mockData );
      const containerDom = document.querySelector( '#chart-section' );
      expect( containerDom.classList.contains( 'geolocating' ) ).toBe( false );
    } );
  } );

  describe( 'startLoading()', () => {
    it( 'should add loaded class', () => {
      chart.render();
      chart.startLoading();
      const dataLoadedDom =
        document.querySelector( '#chart-section .data-enabled' );
      expect( dataLoadedDom.classList.contains( 'loading' ) ).toBe( true );
      expect( dataLoadedDom.classList.contains( 'loaded' ) ).toBe( false );
    } );
  } );

  describe( 'finishLoading()', () => {
    it( 'should add loaded class', () => {
      chart.render();
      chart.finishLoading();
      const dataLoadedDom =
        document.querySelector( '#chart-section .data-enabled' );
      expect( dataLoadedDom.classList.contains( 'loading' ) ).toBe( false );
      expect( dataLoadedDom.classList.contains( 'loaded' ) ).toBe( true );
    } );
  } );

  describe( 'setStatus()', () => {
    it( 'should set state to warning status', () => {
      chart.setStatus( RateCheckerChart.STATUS_WARNING );
      const chartDom = document.querySelector( '#chart' );
      const resultAlertDom = document.querySelector( '#chart-result-alert' );
      expect( chartDom.classList.contains( 'warning' ) ).toBe( true );
      expect( resultAlertDom.classList.contains( 'm-notification__visible' ) ).toBe( true );
    } );

    it( 'should throw error with incorrect status', () => {
      function incorrectStatus() {
        chart.setStatus( -1 );
      }
      expect( incorrectStatus ).toThrow();
    } );
  } );

} );
