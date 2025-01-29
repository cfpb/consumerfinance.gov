import {
  checkDom,
  setInitFlag,
  EventObserver,
  instantiateAll,
  Expandable,
  Multiselect,
} from '@cfpb/cfpb-design-system';
import { analyticsSendEvent } from '@cfpb/cfpb-analytics';
import FormModel from '../modules/util/FormModel.js';

const BASE_CLASS = 'o-filterable-list-controls';

/**
 * FilterableListControls
 * @class
 * @classdesc Initializes a new FilterableListControls organism.
 * @param {HTMLElement} element - The DOM element within which to search
 *   for the organism.
 * @returns {FilterableListControls} An instance.
 */
function FilterableListControls(element) {
  const _dom = checkDom(element, BASE_CLASS);
  const _form = _dom.querySelector('form');
  let _expandable;
  let _formModel;

  /**
   * @returns {FilterableListControls|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if (!setInitFlag(_dom)) {
      let UNDEFINED;
      return UNDEFINED;
    }

    _formModel = new FormModel(_form);

    const multiSelects = Multiselect.init();

    const _expandables = Expandable.init(_dom);
    _expandable = _expandables[0];

    // If multiselects exist on the form, iterate over them.
    multiSelects.forEach((multiSelect) => {
      multiSelect.addEventListener('expandbegin', _refreshExpandableHeight);
      multiSelect.addEventListener('collapsebegin', _refreshExpandableHeight);
      multiSelect.addEventListener(
        'selectionsupdated',
        _refreshExpandableHeight,
      );
    });
    window.addEventListener('resize', _refreshExpandableHeight);

    _formModel.init();
    _initAnalyticsEvents.bind(this)();

    return this;
  }

  let timeout;
  /**
   * Refresh the height of the filterable list control's expandable
   * to ensure all its children are visible.
   */
  function _refreshExpandableHeight() {
    window.clearTimeout(timeout);
    if (_expandable.isExpanded()) {
      timeout = window.setTimeout(_expandable.refresh, 250);
    }
  }

  /**
   * Get data layer object.
   * @param {string} action - Name of event.
   * @param {string} label - DOM element label.
   * @param {string} event - Type of event.
   * @param {Function} [callback] - Function to call on GTM submission.
   * @param {number} [timeout] -
   *   Callback invocation fallback time. Default is 500 milliseconds.
   * @returns {object} Data layer object.
   */
  function _getDataLayerOptions(action, label, event, callback, timeout) {
    return {
      event: event || 'Page Interaction',
      action: action,
      label: label || '',
      eventCallback: callback,
      eventTimeout: timeout || 500,
    };
  }

  /**
   * Initialize FilterableListControls events.
   */
  function _initAnalyticsEvents() {
    const label = _expandable.getLabelText();
    let dataLayerArray = [];
    const cachedFields = {};

    _expandable.addEventListener('expandbegin', () => {
      analyticsSendEvent({ action: 'Filter:open', label });
    });

    _expandable.addEventListener('collapsebegin', () => {
      analyticsSendEvent({ action: 'Filter:close', label });
    });

    _form.addEventListener('change', (event) => {
      const field = event.target;

      if (!field) {
        return;
      }
      const action = field.name + ':change';
      cachedFields[field.name] = _getDataLayerOptions(action, field.value);
    });

    _form.addEventListener('submit', (event) => {
      event.preventDefault();
      Object.keys(cachedFields).forEach((key) => {
        dataLayerArray.push(cachedFields[key]);
      });
      dataLayerArray.push(
        _getDataLayerOptions('Filter:submit', label, '', () => {
          _form.submit();
        }),
      );
      dataLayerArray.forEach((payload) => {
        analyticsSendEvent(payload);
      });
      dataLayerArray = [];
    });
  }

  this.init = init;

  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  return this;
}

FilterableListControls.BASE_CLASS = BASE_CLASS;
FilterableListControls.init = () =>
  instantiateAll(`.${BASE_CLASS}`, FilterableListControls);

export default FilterableListControls;
