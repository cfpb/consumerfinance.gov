/* ==========================================================================
   jquery.cf_formValidator
   ========================================================================== */

'use strict';

var $ = require( 'jquery' );
var _validate = require( 'validate' );

var _validator = {
  defaults: {
    inputs: [
      'input[type!="hidden"]:enabled',
      'textarea:enabled',
      'select:enabled'
    ],
    types: [
      'required',
      'email',
      'checkgroup',
      'radiogroup'
    ],
    onFailure: function() {},
    onSuccess: function() {}
  },

  /**
   * Checks whether the passed input should be skipped
   * for the passed test type.
   * @param   {object}  elem The input we're testing.
   * @param   {string}  type The test type we're checking for.
   * @returns {boolean}      Whether this input should be tested for the type.
   */
  _skipType: function( elem, type ) {
    var typeAttr = elem.attr( 'type' );
    var skips = {
      required:   !elem.prop( 'required' ),
      email:      typeAttr !== 'email',
      radiogroup: typeAttr !== 'radio',
      checkgroup: typeAttr !== 'checkbox'
    };
    return skips[type];
  },

  /**
   * Validate an individual input for each of the set types.
   * @param   {object} elem The jQuery object of the input.
   * @returns {object}      The status of each of the tested types.
  */
  _validateTypes: function( elem ) {
    var status = {};
    var value = elem.val();
    var validation = {
      required: _validate.single( value, { presence: true } ),
      email:    _validate.single( value, { email: true } )
    };

    $.each( _validator.settings.types, function( key, val ) {
      if ( _validator._skipType( elem, val ) ) {
        status[val] = null;
        return false;
      }
      status[val] = typeof validation[val] === 'undefined';
    } );

    return status;
  },

  /**
   * @param   {object} elem The input we're testing.
   * @returns {object}      The formatted validation object
   *                        of the tested input.
   */
  _validateInput: function( elem ) {
    return {
      elem:   elem,
      value:  elem.val(),
      label:  $.trim( $( 'label[for="' + elem.attr( 'id' ) + '"]' ).text() ),
      status: _validator._validateTypes( elem )
    };
  },

  /**
   * @param   {object} elem The check group we're testing.
   * @returns {object}      The formatted validation object
   *                        of the tested check group.
   */
  _validateCheckGroup: function( elem ) {
    return {
      elem:   elem,
      value:  null,
      label:  $.trim( elem.find( '.form-label-header' ).text() ),
      status: {
        checkgroup: elem.find( 'input:checked' ).length > 0
      }
    };
  },

  /**
   * Validate the fields of our form.
   * @param   {object} fields  The list of input fields we're testing.
   * @returns {object}         The tested list of fields broken into valid
   *                           and invalid blocks.
  */
  _validateFields: function( fields ) {
    var checkgroups = {};
    var validatedFields = {
      valid:   [],
      invalid: []
    };

    fields.each( function() {
      var $input = $( this );
      var failed = false;
      var field;

      // If it's a button elem or type is button or submit, skip it.
      if ( $input.is( 'button, :button, :submit' ) ) {
        return;
      // If it's a checkbox test the entire check group.
      } else if ( $input.is( ':checkbox' ) ) {
        var name = $input.attr( 'name' );
        var $group = $input.closest( '.form-group' );
        if ( checkgroups[name] || !$group.hasClass( 'required-check-group' ) ) {
          return;
        }
        field = _validator._validateCheckGroup( $group );
        checkgroups[name] = true;
      } else {
        field = _validator._validateInput( $input );
      }

      for ( var prop in field.status ) {
        if ( field.status[prop] === false ) {
          failed = true;
        }
      }

      if ( failed ) {
        validatedFields.invalid.push( field );
      } else {
        validatedFields.valid.push( field );
      }
    } );

    return validatedFields;
  },

  // Listen for cf_formValidator submit event.
  _initSubmitListener: function() {
    _validator.elem.on( 'submit.cf_formValidator', function( event ) {
      var $submitted = $( this );
      var fields = $submitted.find( _validator.settings.inputs.toString() );
      var validatedFields = _validator._validateFields( fields );

      if ( validatedFields.invalid.length && _validator.settings.onFailure ) {
        _validator.settings.onFailure.call( this, event, validatedFields );
      } else if ( _validator.settings.onSuccess ) {
        _validator.settings.onSuccess.call( this, event, validatedFields );
      }
    } );
  },

  // Remove cf_formValidator submit listeners.
  _rmSubmitListener: function() {
    _validator.elem.off( 'submit.cf_formValidator' );
  },

  init: function( options ) {
    return this.each( function() {
      _validator.elem = $( this );
      _validator.settings = $.extend( {}, _validator.defaults, options );
      _validator._initSubmitListener();
    } );
  },

  destroy: function() {
    return this.each( function() {
      _validator._rmSubmitListener();

      _validator.settings = [];
    } );
  }
};

function init() {
  $.fn.cf_formValidator = function() {
    var options;
    var method = arguments[0];

    if ( _validator[method] ) {
      method = _validator[method];
      options = Array.prototype.slice.call( arguments, 1 );
    } else if ( typeof method === 'object' || !method ) {
      method = _validator.init;
      options = arguments;
    } else {
      $.error(
        'Method "' + method + '" does not exist in the cf_formValidator plugin'
      );
      return this;
    }

    return method.apply( this, options );
  };
}

module.exports = { init: init };
