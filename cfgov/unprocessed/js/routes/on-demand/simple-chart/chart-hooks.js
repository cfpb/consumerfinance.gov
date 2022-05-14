/* eslint camelcase: [0] */
const cci_quarterRange = {
  'Mar 31': 'Jan-Mar',
  'Jun 30': 'Apr-Jun',
  'Sep 30': 'Jul-Sep',
  'Dec 31': 'Oct-Dec'
};

const cci_quarterMap = {
  'Mar 31': 'Q1',
  'Jun 30': 'Q2',
  'Sep 30': 'Q3',
  'Dec 31': 'Q4'
};

const msYear = 365 * 24 * 60 * 60 * 1000;

const hooks = {
  // Example transform
  monotonicY( data ) {
    return data.map( ( item, i ) => ( {
      ...item,
      y: i + 1
    } ) );
  },

  getDateString( x ) {
    return new Date( x ).toLocaleDateString(
      'en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' }
    );
  },

  cci_quarterLabels() {
    const { x, y, series } = this;
    const titleObj = series.yAxis.axisTitle;
    const title = titleObj ? titleObj.textStr + ': ' : '';
    const [ quarter, year ] = hooks.cci_dateToQuarter( x );
    return `<b>${ series.name }</b><br/>${ quarter } ${ year }<br/>${ title }${ Math.round( y * 10 ) / 10 }`;
  },

  cci_dateToQuarter( x ) {
    const d = hooks.getDateString( x ).split( ', ' );
    const quarter = `${ cci_quarterMap[d[0]] }: ${ cci_quarterRange[d[0]] }`;
    const year = d[1];
    return [ quarter, year ];
  },

  cci_tickPositioner() {
    const { series, min, max } = this;
    if ( ( max - min ) / msYear > 5 ) return this.tickPositions;
    let ticks = series[0].xData.filter( v => v >= min && v <= max );
    if ( ticks.length > 9 ) {
      ticks = ticks.filter( ( v, i ) => i % 2 === 0 );
    }
    return ticks;
  },

  cci_xAxisLabels() {
    const { min, max } = this.chart.xAxis[0];
    const d = new Date( this.value );
    if ( ( max - min ) / msYear > 5 ) {
      return d.getFullYear() + 1;
    }

    const dSplit = hooks.getDateString( d ).split( ', ' );
    return `${ cci_quarterMap[dSplit[0]] }<br/>${ dSplit[1] }`;
  },

  enforcement_yAxisLabelsFormatter() {
    return `$${ Math.round( this.value / 1e9 ) }B`;
  },

  enforcement_barTooltipFormatter() {
    return `<b>${ this.x }</b><br/>Total enforcement actions: <b>${ this.y }</b>`;
  },

  enforcement_reliefBarTooltipFormatter() {
    return `<b>${ this.x }</b><br/>Total relief: <b>$${ this.y.toLocaleString() }</b>`;
  },

  cct_credit( data ) {
    const raw = {};
    const adjusted = {};
    data.forEach( v => {
      let currRaw, currAdj;
      if ( raw[v.date] ) {
        currRaw = raw[v.date];
        currAdj = adjusted[v.date];
      } else {
        currRaw = raw[v.date] = { date: v.date, adjusted: 'Unadjusted' };
        currAdj = adjusted[v.date] = { date: v.date, adjusted: 'Seasonally adjusted' };
      }
      currRaw[v.credit_score_group] = v.vol_unadj;
      currAdj[v.credit_score_group] = v.vol;
    } );

    const newData = [];
    [ adjusted, raw ].forEach( obj => {
      for ( const [ , v ] of Object.entries( obj ) ) {
        newData.push( v );
      }
    } );

    return newData.sort( ( a, b ) => new Date( a.date ) - new Date( b.date ) );
  },

  // Rename YoY fields and convert them from decimals to percentages
  cct_credit_yoy( data ) {
    data = data.map( v => ( {
      'date': v.date,
      'Deep subprime': Math.round( v['deep-subprime_yoy'] * 10000 ) / 100,
      'Near prime': Math.round( v['near-prime_yoy'] * 10000 ) / 100,
      'Prime': Math.round( v.prime_yoy * 10000 ) / 100,
      'Subprime': Math.round( v.subprime_yoy * 10000 ) / 100,
      'Super-prime': Math.round( v['super-prime_yoy'] * 10000 ) / 100
    } ) );

    return data.sort( ( a, b ) => new Date( a.date ) - new Date( b.date ) );
  }

};

export default hooks;
