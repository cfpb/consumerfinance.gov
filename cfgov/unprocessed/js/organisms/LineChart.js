'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var standardType = require( '../modules/util/standard-type' );
var chartBuilder = require( 'cfpb-chart-builder' );
var d3 = require( 'd3' );
var formatDate = require( '../modules/util/format-date.js' );
var strToNum = require( '../modules/util/string-to-number.js' );
var formatTime = d3.utcFormat( '%b %Y' );
var parseTime = d3.utcParse( '%Y-%m-%d' );

// Get from HTML.
// var charts = require( './templates/charts.js' );
var DATA_FILE_PATH = 'https://raw.githubusercontent.com/cfpb/consumer-credit-trends/master/data/';

/**
 * LineChart
 * @class
 *
 * @classdesc Initializes a new LineChart molecule.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the molecule.
 * @returns {LineChart} An instance.
 */
function LineChart( element ) { // eslint-disable-line max-statements, inline-comments, max-len

  var BASE_CLASS = 'm-chart-image';

  var _dom = atomicHelpers.checkDom( element, BASE_CLASS );

  /**
   * @returns {LineChart|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }
    
    var chart = element;

    // add defaults for this in back end
    var chartProps = {
      title: chart.getAttribute( 'data-title' ),
      chartType: chart.getAttribute( 'data-chart-type' ),
      source: chart.getAttribute( 'data-source' ),
      BASE_CLASS: BASE_CLASS,
      group: chart.getAttribute( 'group' ), // add to back end
      yAxisUnit: _defineYAxisUnit( chart.getAttribute( 'data-source' ) )
    };

    chartProps.dataUrl = DATA_FILE_PATH + chartProps.source;
    makeDataIntoLineCharts( chartProps );

    return this;
  }

  this.init = init;

  return this;

}


// ******** //
// HELPER FUNCTIONS
// ******** //

function _defineYAxisUnit( fileName ) {
  var yValue = 'B'; // M for Millions, B for Billions
  var numberData = /num_/;

  if ( numberData.test( fileName ) ) {
    yValue = 'M';
  }

  return yValue;
}

function makeDataIntoLineCharts( chartInfo ) {

  d3.csv( chartInfo.dataUrl, function( error, rawData ) {

    var defaultOpts = {
      baseWidth: 650,
      baseHeight: 500,
      paddingDecimal: .1,
      margin: {
        top: 85, right: 20, bottom: 50, left: 75
      }
    }

    var data = rawData;
    if ( chartInfo.group !== null ) {
      var dataGroups = separateLineDataGroups( rawData );
      data = dataGroups[chartInfo.group];
    }

    var maxMonth = getMaxMonth( data );

    data = reformatLineData( data, maxMonth, chartInfo.group !== null );

    chartInfo.yAxisTickFactor = Math.pow( 10, 9 );
    chartInfo.yAxisLabel = 'Volume of Originations (in billions of dollars)'

    if ( chartInfo.yAxisUnit === 'M' ) {
      chartInfo.yAxisTickFactor = Math.pow( 10, 6 );
      chartInfo.yAxisLabel = 'Number of Originations (in millions)'
    }

    var props = {
      data: data,
      // todo: refactor Chart Builder to not require a selector; atomic cfgov-refresh JS should take care of selection
      selector: '.' + chartInfo.BASE_CLASS + '[data-title="' + chartInfo.title + '"]',
      yAxisTickFactor: chartInfo.yAxisTickFactor,
        lineSets: {
          'Unadjusted': {
            classes: 'line line__unadjusted',
            showInLegend: true
          },
          'Unadjusted Projected': {
            classes: 'line line__unadjusted line__projected',
            showInLegend: false
          },
          'Seasonally Adjusted': {
            classes: 'line line__adjusted',
            showInLegend: true
          },
          'Seasonally Adjusted Projected': {
            classes: 'line line__adjusted line__projected',
            showInLegend: false
          }
        },
        labels: {
          yAxisLabel: chartInfo.yAxisLabel,
          yAxisUnit: chartInfo.yAxisUnit
        }
    };

      var line = new chartBuilder.lineChart( props );
      var lineChart = line.drawGraph( defaultOpts );
      addProjectedToLine( lineChart, maxMonth - 6,
        defaultOpts.baseHeight - defaultOpts.margin.top - defaultOpts.margin.bottom );

  } );
}

// find the latest month
function getMaxMonth( rawData ) {
  // find the latest month
  var maxMonth = 0;
  for ( var x = 0; x < rawData.length; x++ ) {
    if ( +rawData[x].month > maxMonth ) {
      maxMonth = +rawData[x].month;
    }
  };

  return maxMonth;
}

// reformat the csv data into a format for chart-builder
function reformatLineData( rawData, maxMonth, multiGroup ) {
  var copies = [],
      data = [];
  // format the rawdata
  for ( var x = 0; x < rawData.length; x++ ) {
    var obj = {};
    obj.x = parseTime( formatDate( +rawData[x].month ) );
    obj.y = +rawData[x].num || +rawData[x].volume;
    obj.y = Math.floor( obj.y );
    if ( multiGroup === true ) {
      obj.set = rawData[x].seasonal
    } else {
      obj.set = rawData[x].group;
    }

    // if the data is exactly seven months old, make a copy for Projected
    if ( +rawData[x].month === maxMonth - 6 ) {
      copies.push( {
        x: obj.x,
        y: obj.y,
        set: obj.set
      } );
    }

    // If data is from last seven months, add 'Projected' to set
    if ( +rawData[x].month >= maxMonth - 6 ) {
      obj.set += ' Projected'
    } 

    // add data if it's 2009 or after
    if ( obj.x >= parseTime( '2009-01-01') ) {
      data.push( obj );
    }
  };

  // Now the copies need to go back in. This allows the Projected line to
  // start at the end of the non-Projected line!
  data = data.concat( copies );

  return data;
}

function addProjectedToLine( chartObject, date, height ) {
  var date = parseTime( formatDate( date ) ),
      x = chartObject.x,
      y = chartObject.y;

  var line = chartObject.chart.append( 'line' )
      .attr( 'x1', x( date ) )
      .attr( 'x2', x( date ) )
      .attr( 'y1', -30 )
      .attr( 'y2', height )
      .classed( 'axis__projected', true);

  chartObject.chart.append( 'text' )
      .attr('x', x( date ) )
      .attr('y', -60 )
      .attr( 'class', 'gray-text' )
      .style( 'text-anchor', 'end' )
      .text( 'Values after ' + formatTime( date ) );
  
  chartObject.chart.append( 'text' )
      .attr( 'x', x( date ) )
      .attr( 'y', -40 )
      .attr( 'class', 'gray-text' )
      .style( 'text-anchor', 'end' )
      .text( 'are projected' )
}

function separateLineDataGroups( rawData ) {
    var obj = {};

    for (var x = 0; x < rawData.length; x++ ) {
      if ( !obj.hasOwnProperty( rawData[x].group ) ) {
        obj[rawData[x].group] = [];
      }
      obj[rawData[x].group].push( rawData[x] );
    }

    return obj;
}

module.exports = LineChart;
