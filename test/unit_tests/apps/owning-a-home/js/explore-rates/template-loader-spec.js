const BASE_JS_PATH = '../../../../../../cfgov/unprocessed/apps/owning-a-home/';
const templateLoader = require(
  BASE_JS_PATH + 'js/explore-rates/template-loader'
);

describe( 'explore-rates/template-loader', () => {

  it( 'should be able to render county template', () => {
    /* eslint-disable camelcase */
    const mockData = {
      complete_fips: 1,
      gse_limit: 1,
      fha_limit: 1,
      va_limit: 1,
      county: 'Test'
    };
    /* eslint-enable camelcase */

    const testTemplate = templateLoader.county( mockData );
    expect( testTemplate ).toBe(
      '<option value="1" data-gse="1" data-fha="1" data-va="1">Test</option>\n'
    );
  } );

  it( 'should be able to render countyConfWarning template', () => {
    const testTemplate = templateLoader.countyConfWarning();
    expect( typeof testTemplate ).toBe( 'string' );
  } );

  it( 'should be able to render countyFHAWarning template', () => {
    const testTemplate = templateLoader.countyFHAWarning();
    expect( typeof testTemplate ).toBe( 'string' );
  } );

  it( 'should be able to render countyVAWarning template', () => {
    const testTemplate = templateLoader.countyVAWarning();
    expect( typeof testTemplate ).toBe( 'string' );
  } );

  it( 'should be able to render countyGenWarning template', () => {
    const testTemplate = templateLoader.countyGenWarning();
    expect( typeof testTemplate ).toBe( 'string' );
  } );

  it( 'should be able to render chartTooltipSingle template', () => {
    const testTemplate = templateLoader.chartTooltipSingle();
    expect( typeof testTemplate ).toBe( 'string' );
  } );

  it( 'should be able to render chartTooltipMultiple template', () => {
    const mockData = {
      y: 1,
      key: '50%'
    };
    const testTemplate = templateLoader.chartTooltipMultiple( mockData );
    expect( testTemplate ).toBe(
      '<div class="chart-tooltip">\n' +
      '  <strong class="lenders">1</strong>\n' +
      '  <span class="text">\n' +
      '    Lenders are offering <br>\n' +
      '    rates at <strong>50%</strong>.\n' +
      '  </span>\n' +
      '</div>\n'
    );
  } );
} );
