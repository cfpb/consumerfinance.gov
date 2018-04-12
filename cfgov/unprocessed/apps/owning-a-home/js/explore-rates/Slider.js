// Required modules.
import { checkDom, setInitFlag }
  from '../../../../js/modules/util/atomic-helpers';
import { UNDEFINED }
  from '../../../../js/modules/util/standard-type';
import { getSelection } from './dom-values';
import rangesliderJs from 'rangeslider-js';

/**
 * Slider
 * @class
 *
 * @classdesc Initializes the organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {Slider} An instance.
 */
function Slider( element ) {
  const BASE_CLASS = 'a-range';
  const _dom = checkDom( element, BASE_CLASS );
  const _inputDom = _dom.querySelector( `.${ BASE_CLASS }_input` );
  const _labelMinDom = _dom.querySelector( `.${ BASE_CLASS }_labels-min` );
  const _labelMaxDom = _dom.querySelector( `.${ BASE_CLASS }_labels-max` );
  const _labelDom = _dom.querySelector( `.${ BASE_CLASS }_text` );

  let _rangeSliderHandleDom;

  let _options;
  let _min;
  let _max;
  let _valMin;
  let _valMax;
  let _lastValue;
  let _currentState;

  // How many units should each step cover.
  const UNITS_PER_STEP = 20;

  /**
   * @param {Object} options - Options to pass to rangeslider-js
   *   (see https://github.com/stbaer/rangeslider-js#options).
   * @returns {Slider|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init( options ) {
    if ( !setInitFlag( _dom ) ) {
      return UNDEFINED;
    }

    _options = options;
    _min = options.min;
    _max = options.max;
    const division = Math.floor( ( _max - _min ) / UNITS_PER_STEP );
    options.step = ( _max - _min ) / division;

    _lastValue = ( _max - _min ) % options.step;

    _render();
    _update();

    return this;
  }

  /**
   * Initialize the range slider. https://github.com/stbaer/rangeslider-js
   */
  function _render() {
    const options = Object.assign( _options, {
      onInit: () => _update(),
      onSlide: ( position, value ) => _update()
    } );
    rangesliderJs.create( _inputDom, options );
    _rangeSliderHandleDom = _dom.querySelector( '.rangeslider__handle' );
  }

  /**
   * Updates the values used for display in the ranges's label.
   */
  function _updateValues() {
    const currentVal = Number( _inputDom.value );
    const currentStep = Math.round( ( ( currentVal - _min ) + _lastValue ) / _options.step );

    _valMin = _min + ( currentStep * UNITS_PER_STEP );
    _valMax = _valMin + UNITS_PER_STEP - 1;
    if ( _valMax > _max ) {
      _valMax = _max;
    }
  }

  /**
   * Moves the range slider handle to the proper position.
   */
  function _update() {
    const handle = _dom.querySelector( '.rangeslider__handle' );
    const matchPx = /translate\((\d*.*\d*)px,.+\)$/;
    const leftVal = Number(
      handle.style.transform.match( matchPx )[1]
    );

    _updateValues();

    _labelDom.textContent = `${ _valMin } - ${ _valMax }`;
    _labelDom.style.left = leftVal - 9 + 'px';
  }

  function setState( state ) {
    if ( state === Slider.STATUS_WARNING ) {
      _rangeSliderHandleDom.classList.add( 'warning' );
    } else if ( state === Slider.STATUS_OKAY ) {
      _rangeSliderHandleDom.classList.remove( 'warning' );
    } else {
      throw new Error( 'State set in range slider is not supported!' );
    }

    _currentState = state;
  }

  this.init = init;
  this.min = () => _min;
  this.max = () => _max;
  this.valMin = () => _valMin;
  this.valMax = () => _valMax;
  this.currentState = () => _currentState;
  this.setState = setState;

  return this;
}

Slider.STATUS_WARNING = 0;
Slider.STATUS_OKAY = 1;

module.exports = Slider;
