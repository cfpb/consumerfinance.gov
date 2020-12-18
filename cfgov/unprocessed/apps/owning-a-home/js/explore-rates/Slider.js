// Required modules.
import {
  checkDom,
  setInitFlag
} from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
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
   * @returns {Slider} An instance.
   */
  function init( options ) {
    if ( !setInitFlag( _dom ) ) {
      return this;
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
    // This could use Object.assign, but it's not supported in IE11.
    const options = _options;
    options.onInit = () => _update();
    options.onSlide = ( position, value ) => _update();

    rangesliderJs.create( _inputDom, options );
    _rangeSliderHandleDom = _dom.querySelector( '.rangeslider__handle' );
  }

  /**
   * Updates the values used for display in the ranges's label.
   */
  function _updateValues() {
    const currentVal = Number( _inputDom.value );
    const numerator = ( currentVal - _min ) + _lastValue;
    const currentStep = Math.round( numerator / _options.step );

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

  /**
   * Set the state of the slider.
   * @param {number} state 0 = okay, 1 = warning state.
   */
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

Slider.STATUS_OKAY = 0;
Slider.STATUS_WARNING = 1;

export default Slider;
