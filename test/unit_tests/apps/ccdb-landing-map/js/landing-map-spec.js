import 'regenerator-runtime/runtime';
import * as sinon from '../../../../../cfgov/unprocessed/apps/ccdb-landing-map/node_modules/sinon';
import Chart from '../../../../../cfgov/unprocessed/apps/ccdb-landing-map/js/Chart';
import landingMap from '../../../../../cfgov/unprocessed/apps/ccdb-landing-map/js/landing-map';
import { simulateEvent } from '../../../../util/simulate-event';


jest.mock( '../../../../../cfgov/unprocessed/apps/ccdb-landing-map/js/Chart.js' );

const HTML_SNIPPET = `
<section id="chart-section" class="chart">
    <div id="landing-map"><div><span><a></a></span></div></div>
  <div class="per-capita m-btn-group">
    <p>Map Shading</p>
    <button class="a-btn raw selected">Complaints</button>
    <button class="a-btn capita a-btn__disabled">Complaints per 1,000</button>
  </div>
</section>
`;

describe( 'Landing Page App', () => {
  let perCapBtn, rawBtn;

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;
    perCapBtn = document.getElementsByClassName( 'capita' )[0];
    rawBtn = document.getElementsByClassName( 'raw' )[0];

    global.fetch = jest.fn().mockImplementation( url => {
      expect( url ).toEqual( 'https://files.consumerfinance.gov/ccdb/hero-map-3y.json' );
      return new Promise( resolve => {
        resolve( {
          json: function() {
            return [
              { name: 'AK', fullName: 'Alaska', value: 713, issue: 'A', product: 'B', perCapita: 0.9653855787913047 },
              { name: 'AL', fullName: 'Alabama', value: 10380, issue: 'A', product: 'B', perCapita: 2.139866013052358 },
              { name: 'AR', fullName: 'Arkansas', value: 4402, issue: 'A', product: 'B', perCapita: 1.4782010675821977 },
              { name: 'AZ', fullName: 'Arizona', value: 14708, issue: 'A', product: 'B', perCapita: 2.159782177421084 }
            ];
          }
        } );
      } );
    } );
  } );

  afterEach( () => {
    Chart.mockClear();
  } );

  describe( 'Window Resize events', () => {
    let clock;
    beforeEach( () => {
      clock = sinon.useFakeTimers();
    } );

    afterEach( () => {
      clock.restore();
    } );

    it( 'redraws after resize', () => {
      landingMap.init();

      global.innerWidth = 500;
      global.dispatchEvent( new Event( 'resize' ) );

      global.innerWidth = 600;
      global.dispatchEvent( new Event( 'resize' ) );

      global.innerWidth = 700;
      global.dispatchEvent( new Event( 'resize' ) );

      clock.tick( 1000 );

      expect( Chart ).toHaveBeenCalledTimes( 2 );
    } );
  } );
  it( 'should not throw any errors on init', () => {
    landingMap.init();
    expect( perCapBtn.classList.contains( 'a-btn__disabled' ) ).toBeTruthy();
    expect( Chart ).toHaveBeenCalledTimes( 1 );
  } );

  describe( 'Per Capita button', () => {
    it( 'switches classes and link when clicked', () => {
      landingMap.init();
      simulateEvent( 'click', perCapBtn );
      expect( rawBtn.classList.contains( 'selected' ) ).toBeFalsy();
      expect( perCapBtn.classList.contains( 'selected' ) ).toBeTruthy();
      expect( Chart ).toHaveBeenCalledTimes( 2 );
    } );
  } );

  describe( 'Complaints button', () => {
    it( 'does not switch classes when already selected', () => {
      landingMap.init();
      simulateEvent( 'click', rawBtn );
      expect( rawBtn.classList.contains( 'selected' ) ).toBeTruthy();
      expect( perCapBtn.classList.contains( 'selected' ) ).toBeFalsy();
    } );

    it( 'switch classes and links when selected twice', () => {
      landingMap.init();
      simulateEvent( 'click', perCapBtn );
      expect( rawBtn.classList.contains( 'selected' ) ).toBeFalsy();
      expect( perCapBtn.classList.contains( 'selected' ) ).toBeTruthy();

      simulateEvent( 'click', rawBtn );
      expect( rawBtn.classList.contains( 'selected' ) ).toBeTruthy();
      expect( perCapBtn.classList.contains( 'selected' ) ).toBeFalsy();

      expect( Chart ).toHaveBeenCalledTimes( 3 );
    } );
  } );
} );
