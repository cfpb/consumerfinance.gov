import { closest } from '@cfpb/cfpb-atomic-component/src/utilities/dom-traverse.js';

/**
 * FormModel
 * @class
 *
 * @classdesc Initializes a new FormModel utility.
 * This class represents a form as a collection (Map) of the various input
 * fields and their attributes.
 *
 *  It organizes them into the following sets:
 *  - all the field elements
 *  - an array of field elements that should be subject to validation
 *
 * @param {HTMLNode} form - The HTML form to model.
 * @returns {FormModel} An instance.
 */
function FormModel( form ) {
  const _form = form;
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

  const _fieldCache = new Map();

  /**
   * @returns {FormModel} An instance.
   */
  function init() {
    _cacheFields();
    return this;
  }

  /**
   * @returns {Map} A map of fields and field options.
   */
  function getModel() {
    return _fieldCache;
  }

  /**
   * Cache the field options.
   */
  function _cacheFields() {
    const rawElements = _form.elements;
    const validateableElements = [];

    let element;
    let type;
    let isIgnored;
    let isDisabled;
    let isInGroup;
    let groupName;
    let isRequired;

    // Build validateable array from HTMLFormControlsCollection.
    for ( let i = 0, len = rawElements.length; i < len; i++ ) {
      element = rawElements[i];
      type = _getElementType( element );
      isDisabled = element.getAttribute( 'disabled' ) !== null;
      isIgnored = _defaults.ignoreFieldTypes.indexOf( type ) > -1;
      isInGroup = _defaults.groupFieldTypes.indexOf( type ) > -1;

      if ( !isIgnored ) {
        validateableElements.push( element );
      }

      if ( isInGroup ) {
        groupName = element.getAttribute( 'data-group' ) ||
                    element.getAttribute( 'name' );
      }

      isRequired = element.getAttribute( 'data-required' ) !== null ||
                   element.getAttribute( 'required' ) !== null;

      _fieldCache.set(
        element,
        {
          type: type,
          label: _getLabelText( element, false || isInGroup ),
          isInGroup: isInGroup
        }
      );
    }

    _fieldCache.set( 'elements', rawElements );
    _fieldCache.set( 'validateableElements', validateableElements );
  }

  /**
   * Get the text associated with a form field's label.
   * @param {HTMLNode} field A form field.
   * @param {boolean} isInGroup Flag used determine if field is in group.
   * @returns {string} The label of the field.
   */
  function _getLabelText( field, isInGroup ) {
    let labelText = '';
    let labelDom;

    if ( isInGroup ) {
      labelDom = closest( field, 'fieldset' );
      if ( labelDom ) {
        labelDom = labelDom.querySelector( 'legend' );
      }
    } else {
      const selector = `label[for="${ field.getAttribute( 'id' ) }"]`;
      labelDom = _form.querySelector( selector );
    }

    /* TODO: Refactor to support multiselects.
             Multiselects contain a fieldset, but don't have an associated
             legend inside the fieldset, so the label here ends up empty. */
    if ( labelDom ) {
      labelText = labelDom.textContent.trim();
    }

    return labelText;
  }

  /**
   * Retrieve a string representing the type of an element.
   * May be a custom data-type attribute, the type attribute (of INPUT elements)
   * or the lowercased HTML tag name.
   * @param {HTMLNode} elem - The HTML element to check. An input usually.
   * @returns {string} A type string for the element.
   */
  function _getElementType( elem ) {
    return elem.getAttribute( 'data-type' ) ||
           elem.getAttribute( 'type' ) ||
           elem.tagName.toLowerCase();
  }

  this.init = init;
  this.getModel = getModel;
  return this;
}

export default FormModel;
