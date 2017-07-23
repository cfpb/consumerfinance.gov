'use strict';

// Import modules.
var _eventObserver = require( '../util/event-observer' );
var _domHelper = require( '../util/dom-helper' );
var _template = require(
  '../../../templates/prepare-worksheets/input-notes.hbs'
);

function create( options ) {
  return new InputNotes( options );
}

// InputNotes UI element constructor.
function InputNotes( options ) {
  // TODO see if bind() can be used in place of _self = this.
  // Note bind()'s lack of IE8 support.
  var _self = this;
  var _row = options.row;
  var data = {
    text:        _row.text,
    altText:     _row.altText,
    placeholder: options.data.placeholder
  };

  var snippet = _template( data );

  // This appendChild could be replaced by jquery or similar if desired/needed.
  // var node = $(options.container).append($(snippet) );
  var node = _domHelper.appendChild( options.container, snippet, 'tbody' );


  // DOM references.
  var _textDOM = node.querySelector( '.text-col' );
  var _altTextInputDOM = node.querySelector( 'textarea' );


  // Listen for updates to the text or grading buttons.
  _altTextInputDOM.addEventListener( 'keyup', _changedHandler );

  function _changedHandler() {
    _self.dispatchEvent( 'change', { row: _row, data: getState() } );
  }


  // @return [Object] The contents of the text input and the button grade.
  function getState() {
    return {
      text:    _row.text,
      altText: _altTextInputDOM.value
    };
  }

  // @param state [Object] `text` and `altText` values.
  function setState( state ) {
    var text = typeof state.text === 'undefined' ? '' : state.text;
    var altText = typeof state.altText === 'undefined' ? null : state.altText;
    _textDOM.innertext = text;
    _altTextInputDOM.value = altText;
  }

  // Expose instance's public methods.
  this.getState = getState;
  this.setState = setState;

  // Attach additional methods.
  _eventObserver.attach( this );
}

// Expose public methods.
this.create = create;
