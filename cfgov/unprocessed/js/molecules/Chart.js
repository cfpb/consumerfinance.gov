'use strict';

// Required modules.
var atomicHelpers = require( '../modules/util/atomic-helpers' );
var standardType = require( '../modules/util/standard-type' );

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

  var BASE_CLASS = 'm-chart_graphics';

  // // Constants for the state of this Chart.
  // var SUCCESS = 'success';
  // var WARNING = 'warning';
  // var ERROR = 'error';

  // // Constants for the Chart modifiers.
  // var MODIFIER_VISIBLE = BASE_CLASS + '__visible';

  var _dom = atomicHelpers.checkDom( element, BASE_CLASS );
  // var _contentDom = _dom.querySelector( '.' + BASE_CLASS + '_content' );

  // var _currentType;

  /**
   * @returns {Chart|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }

    // // Check and set default type of notification.
    // var classList = _dom.classList;
    // if ( classList.contains( BASE_CLASS + '__' + SUCCESS ) ) {
    //   _currentType = SUCCESS;
    // } else if ( classList.contains( BASE_CLASS + '__' + WARNING ) ) {
    //   _currentType = WARNING;
    // } else if ( classList.contains( BASE_CLASS + '__' + ERROR ) ) {
    //   _currentType = ERROR;
    // }

    console.log('Chart init');

    return this;
  }

  /**
   * @param {number} type The notifiation type.
   * @returns {Chart} An instance.
   */
  // function _setType( type ) {
  //   // If type hasn't changed, return.
  //   if ( _currentType === type ) {
  //     return this;
  //   }

  //   var classList = _dom.classList;
  //   classList.remove( BASE_CLASS + '__' + _currentType );

  //   if ( type === SUCCESS ||
  //        type === WARNING ||
  //        type === ERROR ) {
  //     classList.add( BASE_CLASS + '__' + type );
  //     _currentType = type;
  //   } else {
  //     throw new Error( type + ' is not a supported notification type!' );
  //   }

  //   return this;
  // }
}

module.exports = Chart;
