// Required modules.
import { checkDom, setInitFlag } from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import FilterableListControls from './FilterableListControls';
import Notification from '../molecules/Notification';

const BASE_CLASS = 'o-filterable-list';

/**
 * FilterableList
 * @class
 *
 * @classdesc Initializes a new FilterableList organism.
 * A FilterableList contains a FilterableListControls organism for filtering a
 * set of results, any notifications for the filtered results, and a block
 * of filtered results.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {FilterableList} An instance.
 */
function FilterableList( element ) {
  const _dom = checkDom( element, BASE_CLASS );

  let _filterableListControls;
  let _notificationContainer;
  let _notification;
  let _resultsContainer;

  /**
   * @returns {FilterableListControls} An instance.
   */
  function init() {
    if ( !setInitFlag( _dom ) ) {
      return this;
    }

    _filterableListControls = new FilterableListControls(
      _dom.querySelector( `.${ FilterableListControls.BASE_CLASS }` )
    );
    _filterableListControls.addEventListener(
      'fieldInvalid',
      _fieldInvalidHandler
    );

    _notificationContainer = _dom.querySelector(
      `.${ BASE_CLASS }_notification`
    );
    const notificationDom = _notificationContainer.querySelector(
      `.${ Notification.BASE_CLASS }`
    );
    _notification = new Notification( notificationDom );

    _notification.init();
    _filterableListControls.init();

    _resultsContainer = _dom.querySelector( `.${ BASE_CLASS }_results` );

    return this;
  }

  /**
   * Handle a field marked as invalid in the FilterableListControl instance.
   * @param {Object} event - Faux event object from EventObserver.
   */
  function _fieldInvalidHandler( event ) {
    _notification.update(
      Notification.ERROR,
      event.message
    );

    _notification.show();
    _notificationContainer.classList.remove( 'u-hidden' );
    _resultsContainer.classList.add( 'u-hidden' );
  }

  this.init = init;

  return this;
}

export default FilterableList;
