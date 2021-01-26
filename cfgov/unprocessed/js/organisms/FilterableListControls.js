// Required modules.
import * as validators from '../modules/util/validators';
import {
  checkDom,
  instantiateAll,
  setInitFlag
} from '@cfpb/cfpb-atomic-component/src/utilities/atomic-helpers.js';
import Analytics from '../modules/Analytics';
import ERROR_MESSAGES from '../config/error-messages-config';
import EventObserver from '@cfpb/cfpb-atomic-component/src/mixins/EventObserver.js';
import Expandable from '@cfpb/cfpb-expandables/src/Expandable';
import FormModel from '../modules/util/FormModel';
import Multiselect from '@cfpb/cfpb-forms/src/organisms/Multiselect';

const BASE_CLASS = 'o-filterable-list-controls';
const FIELD_ERROR_CLASS = 'a-text-input__error';
let INVALID_FIELDS = [];

/**
 * FilterableListControls
 * @class
 *
 * @classdesc Initializes a new FilterableListControls organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {FilterableListControls} An instance.
 */
function FilterableListControls( element ) {
  const _dom = checkDom( element, BASE_CLASS );
  const _form = _dom.querySelector( 'form' );
  let _expandable;
  let _formModel;

  /**
   * @returns {FilterableListControls|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !setInitFlag( _dom ) ) {
      let UNDEFINED;
      return UNDEFINED;
    }

    _formModel = new FormModel( _form );

    /* Instantiate multiselects before their containing expandable
       so height of any 'selected choice' buttons is included when
       expandable height is calculated initially. */
    const multiSelectsSelector = `.${ BASE_CLASS } .${ Multiselect.BASE_CLASS }`;
    const multiSelects = instantiateAll( multiSelectsSelector, Multiselect );

    const _expandables = Expandable.init( _dom );
    _expandable = _expandables[0];

    /**
     * Refresh the height of the filterable list control's expandable
     * to ensure all its children are visible.
     */
    function _refreshExpandableHeight() {
      window.setTimeout(
        _expandable.transition.expand.bind( _expandable.transition ),
        250
      );
    }

    // If multiselects exist on the form, iterate over them.
    multiSelects.forEach( multiSelect => {
      multiSelect.addEventListener( 'expandBegin', _refreshExpandableHeight );
      multiSelect.addEventListener( 'expandEnd', _refreshExpandableHeight );
      multiSelect.addEventListener( 'selectionsUpdated', _refreshExpandableHeight );
    } );

    _formModel.init();
    _initAnalyticsEvents.bind( this )();

    return this;
  }

  /**
   * Initialize FilterableListControls events.
   */
  function _initAnalyticsEvents() {
    const label = _expandable.getLabelText();
    const getDataLayerOptions = Analytics.getDataLayerOptions;
    let dataLayerArray = [];
    const cachedFields = {};

    _expandable.transition.addEventListener(
      'expandBegin',
      function sendEvent() { Analytics.sendEvent( 'Filter:open', label ); }
    );

    _expandable.transition.addEventListener(
      'collapseBegin',
      function sendEvent() { Analytics.sendEvent( 'Filter:close', label ); }
    );

    _form.addEventListener( 'change', function sendEvent( event ) {
      const field = event.target;

      if ( !field ) {
        return;
      }
      const action = field.name + ':change';
      cachedFields[field.name] = getDataLayerOptions( action, field.value );
    } );

    const formSubmittedBinded = _formSubmitted.bind( this );
    _form.addEventListener( 'submit', function sendEvent( event ) {
      event.preventDefault();
      Object.keys( cachedFields ).forEach( function( key ) {
        dataLayerArray.push( cachedFields[key] );
      } );
      dataLayerArray.push(
        getDataLayerOptions(
          'Filter:submit',
          label,
          '',
          formSubmittedBinded
        )
      );
      Analytics.sendEvents( dataLayerArray );
      dataLayerArray = [];
    } );
  }

  /**
   * Handle form sumbmission and showing error notification.
   */
  function _formSubmitted() {
    const validatedFields = _validateFields(
      _formModel.getModel().get( 'validateableElements' )
    );

    if ( validatedFields.invalid.length > 0 ) {
      _highlightInvalidFields( validatedFields );
      this.dispatchEvent( 'fieldInvalid', {
        message: _buildErrorMessage( validatedFields.invalid )
      } );
    } else {
      _form.submit();
    }
  }

  /**
   * Build the error message to display within the notification.
   * @param {Array} fields - A list of form fields.
   * @returns {string} A text to use for the error notification.
   */
  function _buildErrorMessage( fields ) {
    let msg = '';
    fields.forEach( validation => {
      msg += `${ validation.label } ${ validation.msg }<br>`;
    } );

    return msg || ERROR_MESSAGES.DEFAULT;
  }

  /**
   * Highlight invalid text fields by giving them an error class.
   * @param {Array} fields - A list of form fields.
   * @returns {Array} An array of invalid fields.
   */
  function _highlightInvalidFields( fields ) {
    INVALID_FIELDS.forEach( field => {
      field.classList.remove( FIELD_ERROR_CLASS );
    } );

    INVALID_FIELDS = [];

    fields.invalid.forEach( validation => {
      const field = validation.field;
      if ( field.type === 'text' || field.type === 'date' ) {
        validation.field.classList.add( FIELD_ERROR_CLASS );
        INVALID_FIELDS.push( validation.field );
      }
    } );

    return INVALID_FIELDS;
  }

  /**
   * Validate the fields of our form.
   * @param {Array} fields A list of form fields.
   * @returns {Object}
   *   The tested list of fields broken into valid and invalid blocks.
   */
  function _validateFields( fields ) {
    const validatedFields = {
      invalid: [],
      valid:   []
    };
    let validatedField;

    fields.forEach( field => {
      let fieldIsValid = true;

      validatedField = _validateField( field );

      let prop;
      for ( prop in validatedField.status ) {
        if ( validatedField.status[prop] === false ) {
          fieldIsValid = false;
        }
      }

      if ( fieldIsValid ) {
        validatedFields.valid.push( validatedField );
      } else {
        validatedFields.invalid.push( validatedField );
      }
    } );

    return validatedFields;
  }

  // TODO: Reduce complexity
  /**
   * Validate the specific field types.
   * @param {HTMLNode} field A form field.
   * @param {string} type The type of field.
   * @param {boolean} isInGroup A boolean that determines if field in a group.
   * @returns {Object} An object with a status and message properties.
   */
  function _validateField( field ) {
    let fieldset;
    const fieldModel = _formModel.getModel().get( field );
    const validation = {
      field:  field,
      // TODO: Change layout of field groups to use fieldset.
      label:  fieldModel.label,
      msg:    '',
      status: null
    };

    if ( fieldModel.isInGroup ) {
      const groupName = field.getAttribute( 'data-group' ) ||
                        field.getAttribute( 'name' );
      const groupSelector = '[name=' + groupName + ']:checked,' +
                            '[data-group=' + groupName + ']:checked';
      fieldset = _form.querySelectorAll( groupSelector ) || [];
    }

    if ( validators[fieldModel.type] ) {
      validation.status = validators[fieldModel.type](
        field, validation, fieldset
      );
    }

    return validators.empty( field, validation );
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
