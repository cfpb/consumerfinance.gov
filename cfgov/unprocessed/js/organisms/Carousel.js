// Required modules.
import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import Analytics from '../modules/Analytics';

const BASE_CLASS = 'o-carousel';
const HIDDEN_CLASS = 'o-carousel_item__hidden';

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
function Carousel( element ) { // eslint-disable-line max-lines-per-function
  const _dom = checkDom( element, BASE_CLASS );
  const _btnPrev = _dom.querySelector( `.${ BASE_CLASS }_btn-prev` );
  const _btnNext = _dom.querySelector( `.${ BASE_CLASS }_btn-next` );

  const _thumbnails = _dom.querySelectorAll( `.${ BASE_CLASS }_thumbnail` );
  const _items = _dom.querySelectorAll( `.${ BASE_CLASS }_item` );
  let _currItemIndex = 0;

  // Track how many unique slides the user has seen in the carousel.
  let _slideVisitCount = 1;
  const ALL_SLIDES_VISITED = Math.pow( 2, _items.length ) - 1;
  let _allSlidesVisited = false;

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
        itemDom.classList.add( HIDDEN_CLASS );
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
    if ( _updateDisplay( _currItemIndex, _currItemIndex - 1 ) ) {
      _sendAnalytics( _currItemIndex, 'Previous Arrow' );
    }
  }

  /**
   * Handle clicks of the next button.
   */
  function _btnNextClicked() {
    if ( _updateDisplay( _currItemIndex, _currItemIndex + 1 ) ) {
      _sendAnalytics( _currItemIndex, 'Next Arrow' );
    }
  }

  /**
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

    if ( _updateDisplay( _currItemIndex, i ) ) {
      _sendAnalytics( i, 'Tab' );
    }
  }

  /**
   * Sends events to our analytics provider.
   *
   * @param {number} newCurrItemIndex - The new index value of the selected item.
   * @param {string} interactionLabel - A label for what called this method.
   */
  function _sendAnalytics( newCurrItemIndex, interactionLabel ) {
    // Send individual event
    Analytics.sendEvent( {
      event: 'Page Interaction',
      action: 'Carousel',
      label: `${ interactionLabel } Clicked: Page ${ _currItemIndex + 1 }`
    } );

    /**
     * Send All Items Seen event if all slides have been visited.
     *
     * We use a bitmask to see if all slides have been visited:
     * 0001 = item one (1 decimal).
     * 0010 = item two (2 decimal).
     * 0100 = item three (4 decimal).
     * 1000 = item four (8 decimal).
     * 1111 = all visited (if there are four items) (15 decimal).
     *
     * We need to map 0, 1, 2, … item indices to bitwise digits to 1, 2, 4, ….
     */
    _slideVisitCount |= Math.pow( 2, newCurrItemIndex );
    if ( _slideVisitCount === ALL_SLIDES_VISITED &&
         _allSlidesVisited !== true ) {
      Analytics.sendEvent( {
        event: 'Page Interaction',
        action: 'Carousel',
        label: 'All Items Seen'
      } );
      _allSlidesVisited = true;
    }
  }

  /**
   * Update which carousel item is being displayed.
   * @param {number} oldCurrItemIndex - The previous index value of the selected item.
   * @param {number} newCurrItemIndex - The new index value of the selected item.
   * @returns {boolean} True if the display was updated, false otherwise.
   */
  function _updateDisplay( oldCurrItemIndex, newCurrItemIndex ) {
    if ( oldCurrItemIndex === newCurrItemIndex ) {
      return false;
    }

    const lastItem = _items[oldCurrItemIndex];
    const lastThumbnail = _thumbnails[oldCurrItemIndex];

    _currItemIndex = newCurrItemIndex;
    if ( _currItemIndex < 0 ) {
      _currItemIndex = _items.length - 1;
    } else if ( _currItemIndex > _items.length - 1 ) {
      _currItemIndex = 0;
    }

    // Update visible slides.
    _items[_currItemIndex].classList.remove( HIDDEN_CLASS );
    lastItem.classList.add( HIDDEN_CLASS );

    _thumbnails[_currItemIndex].classList.add( `${ BASE_CLASS }_thumbnail-selected` );
    lastThumbnail.classList.remove( `${ BASE_CLASS }_thumbnail-selected` );

    return true;
  }

  this.init = init;

  return this;
}

Carousel.BASE_CLASS = BASE_CLASS;

export default Carousel;
