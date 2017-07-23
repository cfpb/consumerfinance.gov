'use strict';

// Import modules.
var domHelper = require( '../util/dom-helper' );
var eventObserver = require( '../util/event-observer' );
var buttonGradingGroup = require( './button-grading-group' );
var _template = require( '../../../templates/prepare-worksheets/input-graded.hbs' );


function create( options ) {
  return new InputGraded( options );
}

// InputGraded UI element constructor.
function InputGraded( options ) {
  // TODO see if bind() can be used in place of _self = this.
  // Note bind()'s lack of IE8 support.
  var _self = this;
  // Load our handlebar templates.
  var _grades = options.data.grades;

  var _row = options.row;

  var templateData = {
    placeholder: options.data.placeholder,
    grades: _grades,
    input: _row
  };
  templateData['is_' + _row.grade] = true;

  var _snippet = _template( templateData );

  // This appendChild could be replaced by jquery or similar if desired/needed.
  var _node = domHelper.appendChild( options.container, _snippet );

  // DOM references.
  var _textInputDOM = _row.required ?
                      null :
                      _node.querySelector( '.input-with-btns_input input' );

  // Add events for handling deletion of the node.
  if ( !_row.required ) {
    var btnDeleteDOM = _node.querySelector( '.btn-input-delete' );
    btnDeleteDOM.addEventListener( 'mousedown', deleteItem, false );
  }

  // Deletes this graded input.
  function deleteItem() {
    _node.parentNode.removeChild( _node );
    _self.dispatchEvent( 'delete', { uid: _row.uid } );
  }

  var _selector = '.input-with-btns_btns .btn';
  var buttonSettings = {
    container: _node,
    selector:  _selector,
    row:       _row,
    grades:    _grades
  };
  var _buttonGradingGroup = buttonGradingGroup.create( buttonSettings );

  // Listen for updates to the text or grading buttons.
  if ( !_row.required ) {
    _textInputDOM.addEventListener( 'keyup', _changedHandler );
  }
  _buttonGradingGroup.addEventListener( 'change', _changedHandler );

  function _changedHandler() {
    _self.dispatchEvent( 'change', { row: _row, data: getState() } );
  }
  // @return [Object] The contents of the text input and the button grade.
  function getState() {
    var obj = {
      grade: _buttonGradingGroup.getGrade()
    };

    if ( !_row.required ) {
      obj.text = _textInputDOM.value;
    }

    return obj;
  }

  // @param state [Object] `text` and `grade` values.
  function setState( state ) {
    var text = typeof state.text === 'undefined' ? '' : state.text;
    var grade = typeof state.grade === 'undefined' ? null : state.grade;
    if ( !_row.required ) {
      _textInputDOM.value = text;
    }
    _buttonGradingGroup.setGrade( grade );
  }

  // Expose instance's public methods.
  // 'deleteItem' is also included earlier.
  this.getState = getState;
  this.setState = setState;

  // Attach additional methods.
  eventObserver.attach( this );
}

// Expose public methods.
this.create = create;
