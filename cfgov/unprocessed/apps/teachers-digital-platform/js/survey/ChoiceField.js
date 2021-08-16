const $ = document.querySelector.bind( document );
const $$ = document.querySelectorAll.bind( document );

class ChoiceField {
  constructor( name ) {
    this.name = name;
    this.inputs = [].slice.call( $$( `.ChoiceField[name="${ name }"]` ) );
    this.value = null;
    [].forEach.call( this.inputs, input => {
      if ( input.checked ) {
        this.value = input.value;
      }
    } );
  }

  changeValue( val ) {
    this.value = val;
    this.inputs.forEach( input => {
      if ( input.value === val ) {
        input.checked = true;
      }
    } );
  }

  /**
   * @returns {HTMLUListElement} The UL of the main set of answers
   */
  getUl() {
    return this.inputs[0].closest( 'ul.ChoiceField' );
  }

  markError() {
    const ul = this.getUl();

    // Check existing alert
    /**
     * @type {HTMLDivElement}
     */
    const error = ul.previousElementSibling;
    if ( error && error.classList.contains( 'a-form-alert' ) ) {
      return;
    }

    /**
     * @type {HTMLDivElement}
     */
    let alert = $( '.tdp-survey-alert--clone' );
    alert = alert.cloneNode( true );
    alert.classList.remove( 'tdp-survey-alert--clone' );

    ul.parentNode.insertBefore( alert, ul );
    alert.removeAttribute( 'hidden' );
  }
}

/**
 * @type {Record<string, ChoiceField>}
 */
ChoiceField.cache = Object.create( null );

ChoiceField.get = name => {
  if ( !ChoiceField.cache[name] ) {
    ChoiceField.cache[name] = new ChoiceField( name );
  }
  return ChoiceField.cache[name];
};

/**
 * @returns {ChoiceField[]} unset choice fields
 */
ChoiceField.findUnsets = () => Object
  .values( ChoiceField.cache )
  .filter( cf => cf.value === null );

/**
 * Synchronize unset choices from the store and set choices to the store.
 *
 * @param {string} key The sessionStorage key
 * @returns {Record<string, any>} The stored choice values
 */
ChoiceField.restoreFromSession = key => {
  const store = JSON.parse( sessionStorage.getItem( key ) || '{}' );
  let update = false;

  const checkCache = ( [ name, grp ] ) => {
    if ( grp.value === null ) {
      if ( typeof store[name] !== 'undefined' ) {
        // Sync storage to radio button
        grp.changeValue( store[name] );
      }
    } else if ( typeof store[name] === 'undefined' ) {
      // Sync pre-selected radio to storage (for testing locally)
      store[name] = grp.value;
      update = true;
    }
  };

  Object.entries( ChoiceField.cache ).forEach( checkCache );

  if ( update ) {
    sessionStorage.setItem( key, JSON.stringify( store ) );
  }

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

/**
 * Init radio buttons
 */
ChoiceField.init = () => {
  // Find them all
  [].forEach.call( $$( 'input.ChoiceField' ), input => {
    ChoiceField.get( input.name );
  } );
};

module.exports = ChoiceField;
