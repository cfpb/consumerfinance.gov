// Required modules.
const Analytics = require( '../modules/Analytics' );
const atomicHelpers = require( '../modules/util/atomic-helpers' );
const ERROR_MESSAGES = require( '../config/error-messages-config' );
const Expandable = require( '../organisms/Expandable' );
const getClosestElement = require( '../modules/util/dom-traverse' ).closest;
const Multiselect = require( '../molecules/Multiselect' );
const Notification = require( '../molecules/Notification' );
const standardType = require( '../modules/util/standard-type' );
const validators = require( '../modules/util/validators' );

/**
 * FilterableListControls
 * @class
 *
 * @classdesc Initializes a new Filterable-List-Controls organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 * @returns {FilterableListControls} An instance.
 */
function FilterableListControls( element ) {
  const BASE_CLASS = 'o-filterable-list-controls';
  const _dom = atomicHelpers.checkDom( element, BASE_CLASS );
  let _expandable;
  const _form = _dom.querySelector( 'form' );
  let _notification;
  let _fieldGroups;

  const _defaults = {
    ignoreFieldTypes: [
      'hidden',
      'button',
      'submit',
      'reset',
      'fieldset'
    ],
    groupFieldTypes: [
      'radio',
      'checkbox'
    ]
  };

  /**
   * @returns {FilterableListControls|undefined} An instance,
   *   or undefined if it was already initialized.
   */
  function init() {
    if ( !atomicHelpers.setInitFlag( _dom ) ) {
      return standardType.UNDEFINED;
    }

    /* instantiate multiselects before their containing expandable
       so height of any 'selected choice' buttons is included when
       expandable height is calculated initially */
    const multiSelects = atomicHelpers.instantiateAll(
      'select[multiple]',
      Multiselect
    );

    /* TODO: FilterableListControls should use expandable
       behavior (FlyoutMenu), not an expandable directly. */
    _expandable = new Expandable( _dom );
    _expandable.init();

    if ( _dom.classList.contains( 'o-filterable-list-controls' ) ) {
      multiSelects.forEach( function( multiSelect ) {
        multiSelect.addEventListener( 'expandBegin', function refresh() {
          window.setTimeout( _expandable.refreshHeight, 250 );
        } );

        multiSelect.addEventListener( 'expandEnd', function refresh() {
          window.setTimeout( _expandable.refreshHeight, 250 );
        } );
      } );
    }

    _notification = new Notification( _dom );
    _notification.init();

    _initEvents();

    return this;
  }

  /**
   * Initialize FilterableListControls events.
   */
  function _initEvents() {
    const labelDom = _dom.querySelector( '.o-expandable_label' );
    let label;
    const getDataLayerOptions = Analytics.getDataLayerOptions;
    let dataLayerArray = [];
    const cachedFields = {};

    if ( labelDom ) {
      label = labelDom.textContent.trim();
    }

    _expandable.addEventListener( 'expandBegin', function sendEvent() {
      Analytics.sendEvent( 'Filter:open', label );
    } );

    _expandable.addEventListener( 'collapseBegin', function sendEvent() {
      Analytics.sendEvent( 'Filter:close', label );
    } );

    _form.addEventListener( 'change', function sendEvent( event ) {
      const field = event.target;

      if ( !field ) {
        return;
      }
      const action = field.name + ':change';
      cachedFields[field.name] = getDataLayerOptions( action, field.value );
    } );

    _form.addEventListener( 'submit', function sendEvent( event ) {
      event.preventDefault();
      Object.keys( cachedFields ).forEach( function( key ) {
        dataLayerArray.push( cachedFields[key] );
      } );
      dataLayerArray.push( getDataLayerOptions( 'Filter:submit', label,
        '', _formSubmitted ) );
      Analytics.sendEvents( dataLayerArray );
      dataLayerArray = [];
    } );
  }

  /**
   * Remove Event listeners.
   */
  function destroy() {
    _form.removeEventListener( 'submit', _formSubmitted );
  }

  /**
   * Handle form sumbmission and showing error notification.
   */
  function _formSubmitted( ) {
    const validatedFields = _validateFields( [].slice.call( _form.elements ) );

    if ( validatedFields.invalid.length > 0 ) {
      _setNotification( _notification.ERROR,
        _buildErrorMessage( validatedFields.invalid ) );
    } else {
      _form.submit();
    }
  }

  /**
   * Build the error message to display within the notification.
   * @param {Array} fields A list of form fields.
   * @returns {string} A text to use for the error notification.
   */
  function _buildErrorMessage( fields ) {
    let msg = '';
    fields.forEach( function( validation ) {
      msg += validation.label + ' ' + validation.msg + '</br>';
    } );

    return msg || ERROR_MESSAGES.DEFAULT;
  }

  /**
   * Validate the fields of our form.
   * @param {HTMLNode} field A form field.
   * @param {string} selector Selector used to retreive the dom element.
   * @param {boolean} isInGroup Flag used determine if field is in group.
   * @returns {string} The label of the field.
   */
  function _getLabelText( field, selector, isInGroup ) {
    let labelText = '';
    let labelDom;

    if ( isInGroup && !selector ) {
      labelDom = getClosestElement( field, 'fieldset' );
      if ( labelDom ) labelDom = labelDom.querySelector( 'legend' );
    } else {
      selector = selector ||
                 'label[for="' + field.getAttribute( 'id' ) + '"]';
      labelDom = _form.querySelector( selector );
    }

    if ( labelDom ) labelText = labelDom.textContent.trim();

    return labelText;
  }

  /**
   * Set the notification type, msg, and visibility.
   * @param {string} type The type of notification to display.
   * @param {string} msg The message to display in the notification.
   * @param {string} methodName The method to use to control visibility
   *                            of the notification.
   */
  function _setNotification( type, msg, methodName ) {
    methodName = methodName || 'show';
    _notification.setTypeAndContent( type, msg );
    _notification[methodName]();
  }

  /**
   * Determines if you should validate a field.
   * @param {HTMLNode} field A form field.
   * @param {string} type The type of field.
   * @param {boolean} isInGroup A boolean that determines if field in a group.
   * @returns {boolean} True if the field should be validated, false otherwise.
   */
  function shouldValidateField( field, type, isInGroup ) {
    const isDisabled = field.getAttribute( 'disabled' ) !== null;
    const isIgnoreType = _defaults.ignoreFieldTypes.indexOf( type ) > -1;
    let shouldValidate = isDisabled === false && isIgnoreType === false;

    if ( shouldValidate && isInGroup ) {
      const name = field.getAttribute( 'data-group' ) ||
                   field.getAttribute( 'name' );
      const isRequired = field.getAttribute( 'data-required' ) !== null;
      const groupExists = _fieldGroups.indexOf( name ) > -1;
      if ( groupExists || isRequired === false ) {
        shouldValidate = false;
      } else {
        _fieldGroups.push( name );
      }
    }

    return shouldValidate;
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

    _fieldGroups = [];

    fields.forEach( function loopFields( field ) {
      let fieldIsValid = true;
      const type = field.getAttribute( 'data-type' ) ||
                   field.getAttribute( 'type' ) ||
                   field.tagName.toLowerCase();
      const isGroupField = _defaults.groupFieldTypes.indexOf( type ) > -1;

      if ( shouldValidateField( field, type, isGroupField ) === false ) return;

      validatedField = _validateField( field, type, isGroupField );

      for ( const prop in validatedField.status ) {
        if ( validatedField.status[prop] === false ) fieldIsValid = false;
      }

      if ( fieldIsValid ) {
        validatedFields.valid.push( validatedField );
      } else {
        validatedFields.invalid.push( validatedField );
      }
    } );

    return validatedFields;
  }

  /**
   * Validate the specific field types.
   * @param {HTMLNode} field A form field.
   * @param {string} type The type of field.
   * @param {boolean} isInGroup A boolean that determines if field in a group.
   * @returns {Object} An object with a status and message properties.
   */
  function _validateField( field, type, isInGroup ) {
    let fieldset;
    const validation = {
      field:  field,
      // TODO: Change layout of field groups to use fieldset.
      label:  _getLabelText( field, '', false || isInGroup ),
      msg:    '',
      status: null
    };

    if ( isInGroup ) {
      const groupName = field.getAttribute( 'data-group' ) ||
                        field.getAttribute( 'name' );
      const groupSelector = '[name=' + groupName + ']:checked,' +
                            '[data-group=' + groupName + ']:checked';
      fieldset = _form.querySelectorAll( groupSelector ) || [];
    }

    if ( validators[type] ) {
      validation.status = validators[type]( field, validation, fieldset );
    }

    return validators.empty( field, validation );
  }

  this.init = init;
  this.destroy = destroy;
  return this;
}

module.exports = FilterableListControls;
