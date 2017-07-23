'use strict';

// Import modules.
var _model = require( './worksheet-model' );
var _domHelper = require( './util/dom-helper' );
var _dataDocument = require( './util/data-document' );

// @param options [Object] Options such as the worksheet type, settings, etc.
// @return [Object] A new Worksheet instance.
function create( options ) {
  return new Worksheet( options );
}

// Constructor for a Worksheet instance.
// @param options [Object] Options such as the worksheet type, settings, etc.
function Worksheet( options ) {
  var _inputsList = {};
  var _inputsGroupDOM;

  var _container = options.container;
  var _worksheetTemplate = options.worksheetTemplate;
  // type of worksheet -- risks, flags, personal goals, financial goals.
  var _type = options.type;
  // type of input used for this worksheet -- graded or notes.
  var _inputType = options.inputType;
  var InputModule = options.InputModule;
  var _worksheetData = options.data;

  loadInto( options );

  function loadInto( options ) {
    // used as a toggle for display of add row/reset buttons in template
    _worksheetData['is_' + _inputType] = true;

    var snippet = _worksheetTemplate( _worksheetData );
    var node = _domHelper.appendChild( _container, snippet );
    _inputsGroupDOM = node.querySelector( '.worksheet-input-group' );

    // Generate input rows.
    _generateInputs( options.rows );

    // Activate add/reset buttons for graded editors.
    if ( _inputType === 'graded' ) {
      _initAddBtn();
      _initResetBtn();
    }
  }

  function _generateInputs( rows ) {
    var len = ( rows || [] ).length;
    var i = 0;

    for ( i; i < len; i++ ) {
      _initInput( rows[i] );
    }
  }

  // Creates and adds event listeners to input.
  // @return [Object] An input module instance.
  function _initInput( row ) {
    var settings = {
      container: _inputsGroupDOM,
      data:      _worksheetData,
      row:       row
    };
    var input = InputModule.create( settings );

    // If input broadcasts events, listen for deletion.
    if ( input.addEventListener ) {
      input.addEventListener( 'change', _inputChanged );
      input.addEventListener( 'delete', _inputDeleted );
    }

    _inputsList[row.uid] = input;

    return input;
  }

  function _initAddBtn() {
    var btnAdd = _container.querySelector( ' .btn-worksheet-add-row' );
    btnAdd.addEventListener( 'mousedown', _addRow, false );
  }

  function _initResetBtn() {
    var btnReset = _container.querySelector( ' .btn-worksheet-reset' );
    btnReset.addEventListener( 'mousedown', _reset, false );
  }

  // @param evt [Object] Event object of the change event.
  function _inputChanged( evt ) {
    _model.setWorksheetRow( _type, evt.row, evt.data );
  }

  // @param evt [Object] Event object of the delete event.
  function _inputDeleted( evt ) {
    var inputId = evt.uid;
    delete _inputsList[inputId];
    _model.deleteWorksheetRow( _type, inputId );
  }

  // @param options [Object] The values/options for the new row data.
  //   If omitted the default input values are used.
  function _addRow( opts ) {
    var row = _model.addWorksheetRow( _type, opts );
    _initInput( row );
  }

  // Reset the state to the default values.
  function _reset() {
    var worksheet = _model.resetWorksheet( _type );
    if ( worksheet ) {
      _inputsGroupDOM.innerHTML = '';
      // TODO: destroy all the inputs
      _inputsList = {};
      _generateInputs( worksheet );
    }
  }

  // Expose instance's methods externally.
  this.loadInto = loadInto;
  this.addRow = _addRow;
  this.reset = _reset;

  // Attach additional methods.
  _dataDocument.attach( this );
}

// Expose methods externally.
this.create = create;
