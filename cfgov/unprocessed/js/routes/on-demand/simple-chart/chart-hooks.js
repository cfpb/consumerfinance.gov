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

  enforcement_reliefTooltipFormatter() {
    const { x, y, name, relief, url } = this.points[0].point.options;
    return (
      `<a style="padding: 15px;" rel="noopener noreferrer" target="_blank" href="${ url }">` +
      `<div style="margin-bottom:0.5em"><b>${ new Date( x ).toLocaleDateString(
        'en-US',
        {
          dateStyle: 'medium'
        }
      ) }</b><br/>` +
      `Total relief to date: <b>$${ y.toLocaleString() }</b></div>` +
      `<span class="a-link" style="max-width: 290px; font-weight:500;">${ name }</span><br/>` +
      `Relief from action: <b>$${ relief }</b></a>`
    );
  },

  enforcement_yAxisLabelsFormatter() {
    return `$${ Math.round( this.value / 1e9 ) }B`;
  },

  enforcement_actionsTooltipFormatter() {
    const { x, y, name, url } = this.points[0].point.options;
    return (
      `<a style="padding: 15px;" rel="noopener noreferrer" target="_blank" href="${ url }">` +
      `<div style="margin-bottom:0.5em"><b>${ new Date( x ).toLocaleDateString(
        'en-US',
        {
          dateStyle: 'medium'
        }
      ) }</b><br/>` +
      `Total actions to date: <b>${ y }</b></div>` +
      `<span class="a-link" style="max-width: 290px; font-weight:500;">${ name }</span></a>`
    );
  },

  enforcement_barTooltipFormatter() {
    const { y, name } = this.points[0].point.options;
    return `<b>${ name }</b><br/>Total enforcement actions: <b>${ y }</b>`;
  },

  enforcement_reliefBarTooltipFormatter() {
    const { y, name } = this.points[0].point.options;
    return `<b>${ name }</b><br/>Total relief: <b>$${ y.toLocaleString() }</b>`;
  }
};

export default hooks;
