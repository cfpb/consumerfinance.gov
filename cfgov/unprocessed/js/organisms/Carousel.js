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

  const _thumbnails = _dom.querySelectorAll( `.${ BASE_CLASS }_thumbnail` );
  const _items = _dom.querySelectorAll( `.${ BASE_CLASS }_item` );
  let _currItemIndex = 0;

  /**
   * @returns {Carousel} An instance.
   */
  function init() {
    if ( !setInitFlag( _dom ) ) {
      return this;
    }

    // Create carousel item instances.
    let itemDom;
    for ( let i = 0, len = _items.length; i < len; i++ ) {
      itemDom = _items[i];
      if ( i > 0 ) {
        itemDom.classList.add( 'u-alpha-0' );
      }
    }

    _btnPrev.addEventListener( 'click', _btnPrevClicked );
    _btnNext.addEventListener( 'click', _btnNextClicked );

    for ( let j = 0, len = _thumbnails.length; j < len; j++ ) {
      _thumbnails[j].addEventListener( 'click', _thumbnailClicked );
    }

    // Carousel ready, show it!
    element.classList.remove( 'u-hidden' );

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
   *
   * @param {MouseEvent} event - The event object corresponding to the mouse click of a thumbnail.
   */
  function _thumbnailClicked( event ) {
    let node = event.currentTarget;
    // Get thumbnail index.
    let i = 0;
    while ( ( node = node.previousSibling ) !== null ) {
      if ( node.nodeType === 1 ) {
        ++i;
      }
    }
    if ( _currItemIndex !== i ) {
      _updateDisplay( _currItemIndex, i );
    }
  }

  /**
   * Update which carousel item is being displayed.
   * @param {number} oldCurrItemIndex - The previous index value of the selected item.
   * @param {number} newCurrItemIndex - The new index value of the selected item.
   */
  function _updateDisplay( oldCurrItemIndex, newCurrItemIndex ) {
    const lastItem = _items[oldCurrItemIndex];
    const lastThumbnail = _thumbnails[oldCurrItemIndex];

    _currItemIndex = newCurrItemIndex;
    if ( _currItemIndex < 0 ) {
      _currItemIndex = _items.length - 1;
    } else if ( _currItemIndex > _items.length - 1 ) {
      _currItemIndex = 0;
    }
    _items[_currItemIndex].classList.remove( 'u-alpha-0' );
    lastItem.classList.add( 'u-alpha-0' );

    _thumbnails[_currItemIndex].classList.add( `${ BASE_CLASS }_thumbnail-selected` );
    lastThumbnail.classList.remove( `${ BASE_CLASS }_thumbnail-selected` );
  }

  this.init = init;

  return this;
}

Carousel.BASE_CLASS = BASE_CLASS;

export default Carousel;
