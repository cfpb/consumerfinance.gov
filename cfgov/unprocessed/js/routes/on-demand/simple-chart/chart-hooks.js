/* eslint camelcase: [0] */
const ccpi_quarterRange = {
  'Mar 31': 'Jan-Mar',
  'Jun 30': 'Apr-Jun',
  'Sep 30': 'Jul-Sep',
  'Dec 31': 'Oct-Dec'
};

const ccpi_quarterMap = {
  'Mar 31': 'Q1',
  'Jun 30': 'Q2',
  'Sep 30': 'Q3',
  'Dec 31': 'Q4'
};

const msYear = 365 * 24 * 60 * 60 * 1000;

const hooks = {
  filter( data, filterProp, filterVal ) {
    if ( !filterVal ) return data;
    return data.filter( d => {
      const match = d[filterProp];
      if ( Array.isArray( match ) ) return match.indexOf( filterVal ) >= 0;
      return match === filterVal;
    } );
  },
  // Example transform
  monotonicY( data ) {
    return data.map( ( item, i ) => ( {
      ...item,
      y: i + 1
    } ) );
  },

  ccpi_quarterLabels() {
    const { x, y, series } = this;
    const [ quarter, year ] = hooks.ccpi_dateToQuarter( x );
    return `<b>${ series.name }</b><br/>${ quarter } ${ year }<br/>Index value: ${ Math.round( y * 10 ) / 10 }`;
  },

  ccpi_shareLabels() {
    const { x, y, series } = this;
    const [ quarter, year ] = hooks.ccpi_dateToQuarter( x );
    return `<b>${ series.name }</b><br/>${ quarter } ${ year }<br/>Share: ${ Math.round( y * 10 ) / 10 }%`;
  },

  ccpi_dateToQuarter( x ) {
    const d = new Date( x ).toLocaleString(
      'en-US', { dateStyle: 'medium', timeZone: 'UTC' }
    ).split( ', ' );
    const quarter = `${ ccpi_quarterMap[d[0]] }: ${ ccpi_quarterRange[d[0]] }`;
    const year = d[1];
    return [ quarter, year ];
  },

  ccpi_tickPositioner() {
    const { series, min, max } = this;
    if ( ( max - min ) / msYear > 5 ) return this.tickPositions;
    let ticks = series[0].xData.filter( v => v >= min && v <= max );
    if ( ticks.length > 9 ) {
      ticks = ticks.filter( ( v, i ) => i % 2 === 0 );
    }
    return ticks;
  },

  ccpi_xAxisLabels() {
    const { min, max } = this.chart.xAxis[0];
    const d = new Date( this.value );
    if ( ( max - min ) / msYear > 5 ) {
      return d.getFullYear() + 1;
    }
    const dSplit = d.toLocaleString(
      'en-US', { dateStyle: 'medium', timeZone: 'UTC' }
    ).split( ', ' );
    return `${ ccpi_quarterMap[dSplit[0]] }<br/>${ dSplit[1] }`;
  },

  enforcement_yAxisLabelsFormatter() {
    return `$${ Math.round( this.value / 1e9 ) }B`;
  },

  enforcement_barTooltipFormatter() {
    return `<b>${ this.x }</b><br/>Total enforcement actions: <b>${ this.y }</b>`;
  },

  enforcement_reliefBarTooltipFormatter() {
    return `<b>${ this.x }</b><br/>Total relief: <b>$${ this.y.toLocaleString() }</b>`;
  }
};

export default hooks;
