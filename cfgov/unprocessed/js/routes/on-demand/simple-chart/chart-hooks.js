/* eslint camelcase: [0] */
const ccpi_quarterMap = {
  'Mar 31': 'Q1',
  'Jun 30': 'Q2',
  'Sep 30': 'Q3',
  'Dec 31': 'Q4'
};
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
    const d = new Date( x ).toLocaleString(
      'en-US', { dateStyle: 'medium', timeZone: 'UTC' }
    ).split( ', ' );
    const quarter = ccpi_quarterMap[d[0]];
    const year = d[1];
    return `<b>${ series.name }</b><br/><b>${ quarter } ${ year }</b><br/>Percentile: <b>${ y }</b>`;
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
