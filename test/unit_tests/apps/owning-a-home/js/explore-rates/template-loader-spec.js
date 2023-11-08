import {
  county,
  countyConfWarning,
  countyFHAWarning,
  countyVAWarning,
  countyGenWarning,
  chartTooltip,
} from '../../../../../../cfgov/unprocessed/apps/owning-a-home/js/explore-rates/template-loader.js';

describe('explore-rates/template-loader', () => {
  it('should be able to render county template', () => {
    const mockData = {
      complete_fips: 1,
      gse_limit: 1,
      fha_limit: 1,
      va_limit: 1,
      county: 'Test',
    };

    const testTemplate = county(mockData);
    expect(testTemplate).toBe(
      '<option value="1" data-gse="1" data-fha="1" data-va="1">Test</option>',
    );
  });

  it('should be able to render countyConfWarning template', () => {
    const testTemplate = countyConfWarning;
    expect(typeof testTemplate).toBe('string');
  });

  it('should be able to render countyFHAWarning template', () => {
    const testTemplate = countyFHAWarning;
    expect(typeof testTemplate).toBe('string');
  });

  it('should be able to render countyVAWarning template', () => {
    const testTemplate = countyVAWarning;
    expect(typeof testTemplate).toBe('string');
  });

  it('should be able to render countyGenWarning template', () => {
    const testTemplate = countyGenWarning;
    expect(typeof testTemplate).toBe('string');
  });

  it('should be able to render chartTooltip template with one item', () => {
    const mockData = {
      y: 1,
      key: '50%',
    };
    const testTemplate = chartTooltip(mockData);
    expect(testTemplate).toBe(
      '<div class="chart-tooltip">' +
        '<strong class="lenders">1</strong>' +
        '<span class="text">' +
        'lender is offering <br> ' +
        'rates at <strong>50%</strong>.' +
        '</span>' +
        '</div>',
    );
  });

  it('should be able to render chartTooltip template with multiple items', () => {
    const mockData = {
      y: 3,
      key: '60%',
    };
    const testTemplate = chartTooltip(mockData);
    expect(testTemplate).toBe(
      '<div class="chart-tooltip">' +
        '<strong class="lenders">3</strong>' +
        '<span class="text">' +
        'lenders are offering <br> ' +
        'rates at <strong>60%</strong>.' +
        '</span>' +
        '</div>',
    );
  });
});
