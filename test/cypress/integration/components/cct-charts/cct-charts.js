import { CCTCharts } from './cct-charts-helpers';

const chart = new CCTCharts();

describe( 'CCT Charts', () => {
  it( 'should adjust based on the year range selected', () => {
    chart.open();
    const firstAvailable3yButton = chart.getFirstButton( '3y' ).click();
    firstAvailable3yButton.should( 'have.class', 'highcharts-button-pressed' );
  } );
} );
