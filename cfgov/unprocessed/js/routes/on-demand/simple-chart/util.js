import Analytics from '../../../modules/Analytics.js';

/**
 * Prints an aesthetic time range from a time-aware chart event
 * @param {object} evt  The chart event
 * @returns {string} The formatted time label
 **/
function getChartTitle( evt ) {
  const chartWrapper = evt.target.chart.container.parentNode.parentNode;
  const titleNodes = chartWrapper.getElementsByClassName(
    'o-simple-chart_title'
  );
  if ( titleNodes.length ) return titleNodes[0].textContent;
  return 'Unknown chart title';

}

/**
 * Prints an aesthetic time range from a time-aware chart event
 * @param {object} evt  The chart event
 * @returns {string} The formatted time label
 **/
function getTimeRange( evt ) {
  return `${
    new Date( evt.min ).toLocaleDateString( 'en-US' )
  } - ${ new Date( evt.max ).toLocaleDateString( 'en-US' )
  }`;
}

/**
 * Sends chart event data to Google Analytics
 * @param {object} evt  The chart event
* @param {string} name The action name
* @param {string} label The event label. If absent a time range label will be computed.
 **/
function trackChartEvent( evt, name, label ) {
  if ( !label ) label = getTimeRange( evt );
  Analytics.sendEvent( {
    event: 'Page Interaction',
    action: `${ name }: ${ getChartTitle( evt ) }`,
    label
  } );

}

export default trackChartEvent;
