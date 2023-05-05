import * as validators from '../modules/util/validators.js';
import {
  checkDom,
  setInitFlag,
  EventObserver,
} from '@cfpb/cfpb-atomic-component';
import { analyticsSendEvent } from '@cfpb/cfpb-analytics';
import ERROR_MESSAGES from '../config/error-messages-config.js';
import { Expandable } from '@cfpb/cfpb-expandables';
import FormModel from '../modules/util/FormModel.js';
import { Multiselect } from '@cfpb/cfpb-forms';

const BASE_CLASS = 'o-filterable-list-controls';
const FIELD_ERROR_CLASS = 'a-text-input__error';
let INVALID_FIELDS = [];

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
        _refreshExpandableHeight
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
   * @param {Function} [callback=undefined] - Function to call on GTM submission.
   * @param {number} [timeout=500] - Callback invocation fallback time.
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

    const formSubmittedBinded = _formSubmitted.bind(this);
    _form.addEventListener('submit', (event) => {
      event.preventDefault();
      Object.keys(cachedFields).forEach((key) => {
        dataLayerArray.push(cachedFields[key]);
      });
      dataLayerArray.push(
        _getDataLayerOptions('Filter:submit', label, '', formSubmittedBinded)
      );
      dataLayerArray.forEach((payload) => {
        analyticsSendEvent(payload);
      });
      dataLayerArray = [];
    });
  }

  /**
   * Handle form sumbmission and showing error notification.
   */
  function _formSubmitted() {
    const validatedFields = _validateFields(
      _formModel.getModel().get('validateableElements')
    );

    if (validatedFields.invalid.length > 0) {
      _highlightInvalidFields(validatedFields);
      this.dispatchEvent('fieldinvalid', {
        message: _buildErrorMessage(validatedFields.invalid),
      });
    } else {
      _form.submit();
    }
  }

  /**
   * Build the error message to display within the notification.
   * @param {Array} fields - A list of form fields.
   * @returns {string} A text to use for the error notification.
   */
  function _buildErrorMessage(fields) {
    let msg = '';
    fields.forEach((validation) => {
      msg += `${validation.label} ${validation.msg}<br>`;
    });

    return msg || ERROR_MESSAGES.DEFAULT;
  }

  /**
   * Highlight invalid text fields by giving them an error class.
   * @param {Array} fields - A list of form fields.
   * @returns {Array} An array of invalid fields.
   */
  function _highlightInvalidFields(fields) {
    INVALID_FIELDS.forEach((field) => {
      field.classList.remove(FIELD_ERROR_CLASS);
    });

    INVALID_FIELDS = [];

    fields.invalid.forEach((validation) => {
      const field = validation.field;
      if (field.type === 'text' || field.type === 'date') {
        validation.field.classList.add(FIELD_ERROR_CLASS);
        INVALID_FIELDS.push(validation.field);
      }
    });

    return INVALID_FIELDS;
  }

  /**
   * Validate the fields of our form.
   * @param {Array} fields - A list of form fields.
   * @returns {object} The tested list of fields broken into valid
   *   and invalid blocks.
   */
  function _validateFields(fields) {
    const validatedFields = {
      invalid: [],
      valid: [],
    };
    let validatedField;

    fields.forEach((field) => {
      let fieldIsValid = true;

      validatedField = _validateField(field);

      let prop;
      for (prop in validatedField.status) {
        if (validatedField.status[prop] === false) {
          fieldIsValid = false;
        }
      }

      if (fieldIsValid) {
        validatedFields.valid.push(validatedField);
      } else {
        validatedFields.invalid.push(validatedField);
      }
    });

    return validatedFields;
  }

  // TODO: Reduce complexity
  /**
   * Validate the specific field types.
   * @param {HTMLElement} field - A form field.
   * @returns {object} An object with a status and message properties.
   */
  function _validateField(field) {
    let fieldset;
    const fieldModel = _formModel.getModel().get(field);
    const validation = {
      field: field,
      // TODO: Change layout of field groups to use fieldset.
      label: fieldModel.label,
      msg: '',
      status: null,
    };

    if (fieldModel.isInGroup) {
      const groupName =
        field.getAttribute('data-group') || field.getAttribute('name');
      const groupSelector =
        '[name=' +
        groupName +
        ']:checked,' +
        '[data-group=' +
        groupName +
        ']:checked';
      fieldset = _form.querySelectorAll(groupSelector) || [];
    }

    // eslint-disable-next-line import/namespace
    const validatorsField = validators[fieldModel.type];
    if (validatorsField) {
      validation.status = validatorsField(field, validation, fieldset);
    }

    return validators.empty(field, validation);
  }

  this.init = init;

  const eventObserver = new EventObserver();
  this.addEventListener = eventObserver.addEventListener;
  this.removeEventListener = eventObserver.removeEventListener;
  this.dispatchEvent = eventObserver.dispatchEvent;

  return this;
}

FilterableListControls.BASE_CLASS = BASE_CLASS;

export default FilterableListControls;
