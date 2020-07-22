import { CCTCharts } from '../../components/cct-charts';

const chart = new CCTCharts();

describe( 'CCT Charts', () => {
  it( 'should adjust based on the year range selected', () => {
    chart.open();
    chart.selectTimeRange( '3y' );
    chart.currentTimeRange().should( 'have.text', '3y' );
  } );
} );
