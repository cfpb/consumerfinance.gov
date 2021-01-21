const hooks = {
  filter( data, filterProp, filterVal ) {
    if ( !filterVal ) return data;
    return data.filter( d => {
      const match = d[filterProp];
      if ( Array.isArray( match ) ) return match.indexOf( filterVal ) >= 0;
      return match === filterVal;
    } );
  },

  monotonicY( data ) {
    return data.map( ( item, i ) => ( {
      ...item,
      y: i + 1
    } ) );
  },

  enforcement_relief( data ) {
    const dispositions = [];
    data.forEach( val => {
      const disp = val.enforcement_dispositions;
      if ( disp ) {
        disp.forEach( v => {
          if ( v.final_order_date ) {
            v.url = val.url;
            dispositions.push( v );
          }
        } );
      }
    } );
    dispositions.sort( ( a, b ) => Number( new Date( a.final_order_date ) ) -
      Number( new Date( b.final_order_date ) ) );

    let total = 0;
    return dispositions.map( v => {
      const relief = v.final_order_consumer_redress +
        v.final_order_other_consumer_relief;
      total += relief;

      return {
        x: Number( new Date( v.final_order_date ) ),
        y: total,
        name: v.final_disposition,
        relief: relief,
        url: v.url
      };
    } );
  },


  csv_test( data ) {
    return data.map( d => ( {
      name: d.Quarter,
      y: Number( d['18-30'] )
    } ) );
  },

  csv_datetime( data ) {
    const q2m = { 1: '01', 2: '04', 3: '07', 4: '10' };
    return data.map( d => {
      const qtr = d.Quarter;
      return {
        x: new Date( `${ qtr.slice( 0, 4 ) }-${ q2m[qtr.slice( -1 )] }-01` ),
        y: Number( d['18-30'] )
      };
    } );
  },

  csv_t2( data ) {
    return data.map( d => Number( d['18-30'] )
    );
  },

  csv_cats( data ) {
    return data.map( d => d.name );
  },

  enforcement_counts( data ) {
    const d = data.slice().sort(
      ( a, b ) => Number( new Date( a.initial_filing_date ) ) -
          Number( new Date( b.initial_filing_date ) )
    );

    let total = 0;
    return d.map( v => {
      total++;

      return {
        x: Number( new Date( v.initial_filing_date ) ),
        y: total,
        name: v.public_enforcement_action,
        url: v.url
      };
    } );
  },

  enforcement_reliefCount( data ) {
    const years = {};
    data.forEach( d => {
      const disp = d.enforcement_dispositions;
      if ( disp ) {
        disp.forEach( v => {
          if ( v.final_order_date ) {
            const year = new Date( v.final_order_date ).getFullYear();
            const relief = v.final_order_consumer_redress +
              v.final_order_other_consumer_relief;
            if ( years[year] ) years[year] += relief;
            else years[year] = relief;
          }
        } );
      }
    } );
    return Object.keys( years )
      .sort()
      .map( k => ( { name: k, y: years[k] } ) );
  },

  enforcement_barCount( data ) {
    const years = {};

    data.forEach( d => {
      const year = new Date( d.initial_filing_date ).getFullYear();
      if ( years[year] ) years[year]++;
      else years[year] = 1;
    } );

    return Object.keys( years )
      .sort()
      .map( k => ( { name: k, y: years[k] } ) );
  },


  enforcement_barCategories( { transformed } ) {
    return transformed.map( d => d.name );
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
