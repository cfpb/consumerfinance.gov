'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var standardType = require( '../modules/util/standard-type' );
var LineChart = require( './LineChart.js' );

/**
 * Chart
 * @class
 *
 * @classdesc Initializes a new Chart molecule.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the molecule.
 * @returns {Chart} An instance.
 */
function Chart( element ) { // eslint-disable-line max-statements, inline-comments, max-len

  var BASE_CLASS = 'o-chart';

  var _dom = atomicHelpers.checkDom( element, BASE_CLASS );

  /**
   * @returns {Chart|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }

    console.log('Chart init');

    var svgEl = _dom.querySelector( '.m-chart-image' );


    var lineChart = new LineChart( svgEl );
    lineChart.init();

    return this;
  }

  this.init = init;

  return this;

}

module.exports = Chart;
