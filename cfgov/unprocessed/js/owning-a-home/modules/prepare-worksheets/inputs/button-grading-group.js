'use strict';

// Import modules.
var eventObserver = require( '../util/event-observer' );

function create( options ) {
  return new ButtonGradingGroup( options );
}

// ButtonGradingGroup UI element constructor.
function ButtonGradingGroup( options ) {
  // TODO see if bind() can be used in place of _self = this.
  // Note bind()'s lack of IE8 support.
  var _self = this;

  var _row = options.row;

  var _activeBtn = _row.grade;

  var btnsGradeDOM = options.container.querySelectorAll( options.selector );

  var input;
  for ( var b = 0, len = btnsGradeDOM.length; b < len; b++ ) {
    input = btnsGradeDOM[b];
    input.addEventListener( 'mousedown', gradeSelected( b ) );
  }

  // @param node [Object] The DOM element for the grade selection button.
  // @param btnIndex [Number] The index position of the button.
  function gradeSelected( btnIndex ) {
    return function() {
      // Remove active class from currently selected button.
      if ( _activeBtn !== null && typeof _activeBtn !== 'undefined' ) {
        btnsGradeDOM[_activeBtn].className = btnsGradeDOM[_activeBtn].className.replace( 'active', '' );
      }
      // Set new grade.
      if ( btnIndex === null ||
           typeof btnIndex === 'undefined' ||
           btnIndex === _activeBtn ) {
        // Grade was unset.
        _activeBtn = null;
      } else {
        _activeBtn = btnIndex;
        btnsGradeDOM[btnIndex].className += ' active';
      }
      _self.dispatchEvent( 'change', {
        row:  _row,
        data: { grade: _activeBtn }
      } );
    };
  }

  // TODO: Check if unsetGrades is used somewhere, and if not, remove it.
  function unsetGrades( node ) {
    if ( node ) {
      node.className = node.className.replace( 'active', '' );
    }
    options.container.className = options.container.className.replace( 'active', '' );
    _row.grade = null;
  }

  function getGrade() {
    return _activeBtn;
  }

  function setGrade( toGrade ) {
    gradeSelected( toGrade );
  }

  // Expose public methods
  this.getGrade = getGrade;
  this.setGrade = setGrade;

  // Attach additional methods.
  eventObserver.attach( this );
}

// Expose public methods.
this.create = create;
