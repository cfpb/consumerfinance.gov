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
    onFailure: function( event, fields ) {},
    onSuccess: function( event, fields ) {}
  },

  // Validate an individual input for each of the set types
  // @param   {object} $input The jQuery object of the input
  // @param   {string} value  The evaluated value of the input
  // @returns {object}        The status of each of the tested types
  _validateInput: function( $input, value ) {
    var status = {};

    $.each( _validator.settings.types, function( i ) {
      var validation;
      var type        = this;
      var notRequired = ( type === 'required' && !$input.prop( 'required' ) );
      var notEmail    = ( type === 'email' && $input.attr( 'type') !== 'email' );
      var notRadio    = ( type === 'radiogroup' && $input.attr( 'type' ) !== 'radio' );
      var notCheckbox = ( type === 'checkgroup' && $input.attr( 'type' ) !== 'checkbox' );

      if ( notRequired || notEmail || notRadio || notCheckbox ) {
        status[type] = null;
        return false;
      }

      if ( type === 'required' ) {
        validation = _validate.single( value, { presence: true } );
      } else if ( type === 'email' ) {
        validation = _validate.single( value, { email: true } );
      }
      status[type] = ( validation === undefined );
    } );

    return status;
  },

  // Validate the fields of our form
  // @returns {object} Two inner objects containing the valid and invalid fields
  _validateFields: function( fields ) {
    var checkgroups = {};
    var validatedFields = {
      valid:    [],
      invalid:  []
    };

    fields.each( function( i ) {
      var $input  = $( this );
      var failed  = false;
      var field;

      // if it's a button elem or type is button or submit, skip it
      if ( $input.is( 'button, :button, :submit' ) ) {
        return;
      // if it's a checkbox test the entire check group
      } else if ( $input.is( ':checkbox' ) ) {
        var name    = $input.attr( 'name' );
        var $group  = $input.closest( '.form-group' );

        if ( checkgroups[name] || !$group.hasClass( 'required-check-group' ) ) {
          return;
        }

        var isChecked = $group.find( 'input:checked' ).length > 0;

        field = {
          elem:   $group,
          value:  null,
          label:  $.trim( $group.find( '.form-label-header' ).text() ),
          status: {
            checkgroup: isChecked
          }
        }

        checkgroups[name] = true;
      } else {
        var value       = $input.val();
        var validation  = _validator._validateInput( $input, value );

        field = {
          elem:   $input,
          value:  value,
          label:  $.trim( $( 'label[for="' + $input.attr( 'id' ) + '"]' ).text() ),
          status: validation
        };
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

  // Listen for cf_formValidator submit event
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

  // Remove cf_formValidator submit listeners
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

  destroy: function( options ) {
    return this.each( function() {
      _validator._rmSubmitListener();

      _validator.settings = [];
    });
  }
};

function init() {
  $.fn.cf_formValidator = function() {
    var options;
    var method = arguments[0];

    if ( _validator[method] ) {
      method  = _validator[method];
      options = Array.prototype.slice.call( arguments, 1 );
    } else if ( typeof( method ) === 'object' || !method ) {
      method  = _validator.init;
      options = arguments;
    } else {
      $.error( 'Method "' +  method + '"" does not exist in the cf_formValidator plugin' );
      return this;
    }

    return method.apply( this, options );
  };
}

module.exports = { init: init };
