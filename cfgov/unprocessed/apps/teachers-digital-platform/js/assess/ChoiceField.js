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
  let update = false;

  Object.entries( ChoiceField.cache ).forEach( ( [ name, grp ] ) => {
    if (grp.value !== null && typeof store[name] === 'undefined') {
      // Sync pre-selected radio to storage (for testing locally)
      store[name] = grp.value;
      update = true;
    }

    if (grp.value === null && typeof store[name] !== 'undefined') {
      // Sync storage to radio button
      grp.changeValue( store[name] );
    }
  } );

  if ( update ) {
    sessionStorage.setItem( key, JSON.stringify( store ) );
  }

  return store;
};

ChoiceField.watchAndStore = ( key, store, onStoreUpdate ) => {
  document.addEventListener( 'change', e => {
    const t = e.target;
    if (t instanceof HTMLInputElement && t.classList.contains( 'ChoiceField' )) {
      if (t.checked) {
        ChoiceField.get( t.name ).value = t.value;
        store[t.name] = t.value;
        sessionStorage.setItem( key, JSON.stringify( store ) );
        if ( onStoreUpdate ) {
          onStoreUpdate();
        }
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
