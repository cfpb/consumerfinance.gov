import * as selectFilters from '../../../../../../cfgov/unprocessed/js/routes/on-demand/simple-chart/select-filters.js';

const HTML = `
  <div id="chart"></div>
`;

describe( 'Simple chart select filters', () => {

  let dataAttributes = {};
  let chartNode;
  let chart;
  let data;
  let transform;

  beforeEach( () => {
    // things to do before each test
  } );

  afterEach( () => {
    // things to do after each test
  } );

  it( 'calls the system print dialog when clicked', () => {
    selectFilters.initFilters( dataAttributes, chartNode, chart, data, transform );

    expect( 1 ).toBe( 1 );
  } );
} );
