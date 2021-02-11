const hooks = {
  monotonicY( data ) {
    return data.map( ( item, i ) => ( {
      ...item,
      y: i + 1
    } ) );
  },

  enforcement_barCount( data ) {
    const years = {};
    data.forEach( d => {
      const year = new Date( d.x ).getFullYear();
      if ( years[year] ) years[year]++;
      else years[year] = 1;
    } );
    return Object.keys( years )
      .sort()
      .map( k => ( { name: k, y: years[k] } ) );
  },

  enforcement_reliefCount( data ) {
    const years = {};
    data.forEach( d => {
      const year = new Date( d.x ).getFullYear();
      const relief = Number( d.relief.replace( /[,\.]/g, '' ) ) / 100;
      if ( years[year] ) years[year] += relief;
      else years[year] = relief;
    } );
    return Object.keys( years )
      .sort()
      .map( k => ( { name: k, y: years[k] } ) );
  },

  enforcement_barCategories( data ) {
    return data.map( d => d.name );
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
