// Required modules.
import { checkDom, setInitFlag } from '../modules/util/atomic-helpers';

const BASE_CLASS = 'o-carousel';

/**
 * Carousel
 * @class
 *
 * @classdesc Initializes a new Carousel organism.
 * A Carousel contains a list of CarouselItems for showing/hiding them sequentially.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {Carousel} An instance.
 */
function Carousel( element ) {
  const _dom = checkDom( element, BASE_CLASS );
  const _btnPrev = _dom.querySelector( `.${ BASE_CLASS }_btn-prev` );
  const _btnNext = _dom.querySelector( `.${ BASE_CLASS }_btn-next` );

  const _items = [];
  let _currItemIndex = 0;
  
  /**
   * @returns {Carousel} An instance.
   */
  function init() {
    if ( !setInitFlag( _dom ) ) {
      return this;
    }

    // Grab all carousel item DOM references. 
    let itemDoms = element.querySelectorAll( `.${ BASE_CLASS }_item` );

    // Create carousel item instances.
    let itemDom;
    for ( let i = 0, len = itemDoms.length; i < len; i++ ) {
      itemDom = itemDoms[i];
      _items.push( new CarouselItem( itemDom ) );
      if ( i > 0 ){
        itemDom.classList.add( 'u-hidden' );
      }
    }

    _btnPrev.addEventListener( 'click', _btnPrevClicked );
    _btnNext.addEventListener( 'click', _btnNextClicked );

    return this;
  }

  /**
   * Handle clicks of the previous button.
   */
  function _btnPrevClicked() {
    _updateDisplay( _currItemIndex, _currItemIndex - 1 );
  }

  /**
   * Handle clicks of the next button.
   */
  function _btnNextClicked() {
    _updateDisplay( _currItemIndex, _currItemIndex + 1 );
  }

  /**
   * Update which carousel item is being displayed.
   * @param {number} oldCurrItemIndex - The previous index value of the selected item.
   * @param {number} newCurrItemIndex - The new index value of the selected item.
   */
  function _updateDisplay( oldCurrItemIndex, newCurrItemIndex ) {
    const lastItem = _items[oldCurrItemIndex];
    _currItemIndex = newCurrItemIndex;
    if ( _currItemIndex < 0 ) {
      _currItemIndex = _items.length -1;
    } else if ( _currItemIndex > _items.length - 1 ) {
      _currItemIndex = 0;
    }
    _items[_currItemIndex].show();
    lastItem.hide();
  }

  this.init = init;

  return this;
}

/**
 * Private class for handling carousel item API.
 * @param {HTMLElement} element - Carousel item's DOM element.
 */
function CarouselItem( element ) {
  
  /**
   * Display this carousel item.
   */
  function show() {
    element.classList.remove( 'u-hidden' );
  }

  /**
   * Hide this carousel item.
   */
  function hide() {
    element.classList.add( 'u-hidden' );
  }

  this.show = show;
  this.hide = hide;

  return this;
}

Carousel.BASE_CLASS = BASE_CLASS;

export default Carousel;
