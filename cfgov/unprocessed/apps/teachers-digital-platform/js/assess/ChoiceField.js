const $$ = document.querySelectorAll.bind( document );

class ChoiceField {
  constructor( name ) {
    this.inputs = $$( `.ChoiceField[name="${ name }"]` );
    this.value = null;
    [].forEach.call( this.inputs, input => {
      if (input.checked) {
        this.value = input.value;
      }
    } );
  }

  changeValue( val ) {
    this.value = val;
    [].forEach.call( this.inputs, input => {
      if (input.value === val) {
        input.checked = true;
      }
    } );
  }
}

ChoiceField.cache = Object.create( null );

ChoiceField.get = ( name ) => {
  if (!ChoiceField.cache[name]) {
    ChoiceField.cache[name] = new ChoiceField( name );
  }
  return ChoiceField.cache[name];
};

ChoiceField.restoreFromSession = ( key ) => {
  const store = JSON.parse( sessionStorage.getItem( key ) || '{}' );

  Object.entries( ChoiceField.cache ).forEach( ( [ name, grp ] ) => {
    if (grp.value === null && typeof store[name] !== 'undefined') {
      grp.changeValue( store[name] );
    }
  } );

  return store;
};

ChoiceField.watchAndStore = ( key, store ) => {
  document.addEventListener( 'change', e => {
    const t = e.target;
    if (t instanceof HTMLInputElement && t.classList.contains( 'ChoiceField' )) {
      if (t.checked) {
        ChoiceField.get( t.name ).value = t.value;
        store[t.name] = t.value;
        sessionStorage.setItem( key, JSON.stringify( store ) );
      }
    }
  } );
};

ChoiceField.init = () => {
  // Find them all
  [].forEach.call( $$( '.ChoiceField' ), input => {
    ChoiceField.get( input.name );
  } );
};

module.exports = ChoiceField;
