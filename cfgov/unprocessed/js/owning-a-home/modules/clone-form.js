'use strict';

function _copyRadio( radios, to ) {
  for ( var i = 0, len = radios.length; i < len; i++ ) {
    if ( radios[i].checked ) {
      // targets = to.querySelectorAll('[name^=' + radios[i].name.slice(0, -1) + ']');
      to.querySelector( '[value="' + radios[i].value + '"]' ).checked = true;
      return;
    }
  }
}

function cloneForm( from, to ) {
  if ( !( from = document.querySelector( from ) ) ) {
    throw new Error( 'Source form not found on page.' );
  }
  if ( !( to = document.querySelector( to ) ) ) {
    throw new Error( 'Destination form not found on page.' );
  }

  var fromFields = from.querySelectorAll( '[name]' );
  var el;
  var target;

  for ( var i = 0, len = fromFields.length; i < len; i++ ) {
    el = fromFields[i];
    target = to.querySelector( '[name=' + el.name + ']' );

    if ( el.type !== 'radio' && target ) {
      target.value = el.value;
      continue;
    }

    if ( el.type === 'radio' && target ) {
      el = from.querySelectorAll( '[name=' + el.name + ']' );
      _copyRadio( el, to );
    }
  }

}

module.exports = cloneForm;
