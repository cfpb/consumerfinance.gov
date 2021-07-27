const $ = document.querySelector.bind( document );
const $$ = document.querySelectorAll.bind( document );

class ChoiceField {
  constructor( name ) {
    this.name = name;
    this.inputs = $$( `.ChoiceField[name="${ name }"]` );
    this.value = null;
    [].forEach.call( this.inputs, input => {
      if ( input.checked ) {
        this.value = input.value;
      }
    } );
  }

  changeValue( val ) {
    this.value = val;
    [].forEach.call( this.inputs, input => {
      if ( input.value === val ) {
        input.checked = true;
      }
    } );
  }
}

ChoiceField.cache = Object.create( null );

ChoiceField.get = name => {
  if ( !ChoiceField.cache[name] ) {
    ChoiceField.cache[name] = new ChoiceField( name );
  }

  return ChoiceField.cache[name];
};

ChoiceField.restoreFromSession = key => {
  const store = JSON.parse( sessionStorage.getItem( key ) || '{}' );
  const storeText = JSON.parse( sessionStorage.getItem( key + 'Text' ) || '{}' );

  let update = false;

  const checkCache = ( [ name, cf ] ) => {
    // First label is the question label
    const label = $( `label[for="id_${ name }_0"]` );
    storeText[name] = label ? label.textContent : '';

    if ( cf.value === null ) {
      if ( typeof store[name] !== 'undefined' ) {
        // Sync storage to radio button
        cf.changeValue( store[name] );
      }
    } else if ( typeof store[name] === 'undefined' ) {
      // Sync pre-selected radio to storage (for testing locally)
      store[name] = cf.value;
      update = true;
    }
  };

  Object.entries( ChoiceField.cache ).forEach( checkCache );

  if ( update ) {
    sessionStorage.setItem( key, JSON.stringify( store ) );
  }

  setTimeout( () => {
    sessionStorage.setItem( key + 'Text', JSON.stringify( storeText ) );
  }, 100 );

  return store;
};

ChoiceField.watchAndStore = ( key, store, onStoreUpdate ) => {
  const storeValue = t => {
    ChoiceField.get( t.name ).value = t.value;
    store[t.name] = t.value;
    sessionStorage.setItem( key, JSON.stringify( store ) );
    if ( onStoreUpdate ) {
      onStoreUpdate();
    }
  };

  document.addEventListener( 'change', event => {
    const t = event.target;
    if ( t instanceof HTMLInputElement && t.classList.contains( 'ChoiceField' ) && t.checked ) {
      storeValue( t );
    }
  } );
};

ChoiceField.findUnanswered = () => Object.values( ChoiceField.cache )
  .filter( cf => cf.value === null );

ChoiceField.init = () => {
  // Find them all
  [].forEach.call( $$( 'input.ChoiceField' ), input => {
    ChoiceField.get( input.name );
  } );
};

module.exports = ChoiceField;
