require( './CustomEvent-polyfill' );

let openModals = [];

class Modal {
  constructor( id ) {
    this.id = id;
    this.isOpen = false;
  }

  getElement() {
    return document.querySelector( `#${ this.id }` );
  }

  open() {
    const el = this.getElement();

    const event = new CustomEvent( 'modal:open:before', {
      bubbles: true,
      detail: { modal: this }
    } );
    el.dispatchEvent( event );

    // Allow screen readers to see dialog
    el.setAttribute( 'aria-hidden', 'false' );
    el.classList.add( 'o-modal__visible' );
    const desc = document.querySelector( `#${ this.id }_desc` );
    const focusableSelector = [
      'button',
      'a',
      'input:not([type="hidden"])',
      'select',
      'textarea',
      '[tabindex]:not([tabindex="-1"])'
    ].join( ',' );
    const focusable = desc.querySelector( focusableSelector );
    if ( focusable ) {
      focusable.focus();
    }

    this.isOpen = true;
    openModals.push( this );
  }

  close() {
    this.isOpen = false;
    openModals = openModals.filter( modal => modal.isOpen );

    const el = this.getElement();
    // Hide from screen readers
    el.setAttribute( 'aria-hidden', 'true' );
    el.classList.remove( 'o-modal__visible' );
  }
}

/**
 * Close a modal by ID
 *
 * @param {string} id Modal ID
 */
function close( id ) {
  openModals.forEach( modal => {
    if ( modal.id === id ) {
      modal.close();
    }
  } );
}

/**
 * Initialize events for modals
 */
function init() {
  document.addEventListener( 'click', event => {
    const t = event.target;
    const opener = t.closest( '[data-open-modal]' );
    if ( opener ) {
      event.preventDefault();
      event.stopPropagation();
      const id = opener.dataset.openModal;
      const modal = new Modal( id );
      modal.open();
      return;
    }

    if ( !openModals.length ) {
      return;
    }

    const modal = openModals[openModals.length - 1];
    const closeTopModal = () => {
      modal.close();
      event.stopPropagation();
    };

    const content = modal.getElement().querySelector( '.o-modal_content' );
    if ( content.contains( t ) ) {
      // Close if clicking modal's close button(s)
      if ( content.querySelector( '.o-modal_close' ).contains( t ) ) {
        closeTopModal();
        return;
      }

      // Close if clicked footer button with "close"
      const btn = content.querySelector( '.o-modal_footer button' );
      if ( t === btn && ( /\bclose\b/i ).test( btn.textContent ) ) {
        closeTopModal();
      }
    } else {
      // Outside modal
      closeTopModal();
    }
  } );

  document.addEventListener( 'keydown', event => {
    if ( event.key !== 'Escape' || !openModals.length ) {
      return;
    }

    openModals[openModals.length - 1].close();
    event.stopPropagation();
  } );
}

export { init, close };
