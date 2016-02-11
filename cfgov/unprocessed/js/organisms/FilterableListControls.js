'use strict';

// Required modules.
var atomicCheckers = require( '../modules/util/atomic-checkers' );
var Expandable = require( '../molecules/Expandable' );
var Notification = require( '../molecules/Notification' );
// TODO: Implement form data client-side validation.
// var validate = require( 'validate' );

/**
 * FilterableListControls
 * @class
 *
 * @classdesc Initializes a new Filterable-List-Controls organism.
 *
 * @param {HTMLNode} element
 *   The DOM element within which to search for the organism.
 */
function FilterableListControls( element ) {
  var BASE_CLASS = 'o-filterable-list-controls';

  var _dom = atomicCheckers.validateDomElement(
    element, BASE_CLASS, 'FilterableListControls' );
  var _form = _dom.querySelector( 'form' );
  var _notification;
  var _fields = [];

  var _validatorDefaults = {
    inputs: [
      'input',
      'textarea',
      'select'
    ]
  };

  /**
   * Initialize FilterableListControls instance.
  */
  function init() {
    var expandable = new Expandable( _dom );
    expandable.init();
    _notification = new Notification( _dom );
    _notification.init();
    _form.addEventListener( 'submit', _formSubmitted );

    var inputs = _validatorDefaults.inputs;
    var fields;
    var field;
    var type;
    for ( var i = 0, len = inputs.length; i < len; i++ ) {
      fields = _form.querySelectorAll( inputs[i] );
      for ( var f = 0, flen = fields.length; f < flen; f++ ) {
        field = fields[f];
        type = field.getAttribute( 'type' );
        if ( type !== 'hidden' &&
             type !== 'button' &&
             type !== 'submit' &&
             type !== 'reset' &&
             typeof field.getAttribute( 'disabled' ) !== 'undefined' ) {
          _fields.push( field );
        }
      }
    }
  }

  /**
   * Show error notification.
   * @param {Object} event Form submitted event.
  */
  function _formSubmitted( event ) {
    event.preventDefault();
    var validatedFields = _validateFields( _fields );

    if ( validatedFields.invalid.length > 0 ) {
      _showError();
    } else {
      _showSuccess();
    }
  }

  /**
   * Show error notification.
  */
  function _showError() {
    _notification.setTypeAndContent( _notification.ERROR, 'Error!' );
    _notification.show();
  }

  /**
   * Show success notification.
  */
  function _showSuccess() {
    _notification.setTypeAndContent( _notification.SUCCESS, 'Success!' );
    _notification.show();
  }

  /**
   * Validate the fields of our form.
   * @param  {Array} fields The list of input fields we're testing.
   * @returns {Object}
   *   The tested list of fields broken into valid and invalid blocks.
  */
  function _validateFields( fields ) {
    var checkgroups = {};
    var validatedFields = {
      valid:   [],
      invalid: []
    };

    var field;
    var name;
    for ( var f = 0, flen = fields.length; f < flen; f++ ) {
      field = fields[f];
      name = field.getAttribute( 'name' );
      if ( !checkgroups[name] ) {
        checkgroups[name] = [];
      }
      checkgroups[name].push( field );
    }

    var status;
    for ( var group in checkgroups ) {
      if ( checkgroups.hasOwnProperty( group ) ) {
        status = group.length > 1 ?
                 _validateCheckGroup( group ) : _validateInput( group );

        for ( var prop in status.status ) {
          if ( status.status[prop] === false ) {
            validatedFields.valid.push( field );
          } else {
            validatedFields.invalid.push( field );
          }
        }
      }
    }

    return validatedFields;
  }

  /**
   * @param {Object} elem The check group we're testing.
   * @returns {Object}
   *   The formatted validation object of the tested check group.
   */
  function _validateCheckGroup( elem ) {
    // TODO: Replace mock data with real validation data.
    return {
      elem:   elem,
      value:  null,
      label:  null,
      status: {
        checkgroup: false
      }
    };
  }

  /**
   * @param {Object} elem The input we're testing.
   * @returns {Object} The formatted validation object of the tested input.
   */
  function _validateInput( elem ) {
    // TODO: Replace mock data with real validation data.
    return {
      elem:   elem,
      value:  null,
      label:  null,
      status: false
    };
  }

  this.init = init;
  return this;
}

module.exports = FilterableListControls;
