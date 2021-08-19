require( './CustomEvent-polyfill' );

let openModals = [];

class Modal {
  constructor( id, opener ) {
    this.id = id;
    this.isOpen = false;
    this.opener = opener || null;
    this._addFocusTraps();
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
    el.setAttribute( 'aria-modal', 'true' );
    el.setAttribute( 'role', 'dialog' );
    el.classList.add( 'o-modal__visible' );

    const closer = document.querySelector( `#${ this.id } .o-modal_close` );
    if ( closer ) {
      closer.focus();
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
    el.removeAttribute( 'aria-modal' );
    el.removeAttribute( 'role' );
    el.classList.remove( 'o-modal__visible' );

    if ( this.opener ) {
      this.opener.focus();
    }
  }

  _addFocusTraps() {
    const before = document.createElement( 'a' );
    before.href = '#';
    before.setAttribute( 'data-trap', '0' );
    const after = document.createElement( 'a' );
    after.href = '#';
    after.setAttribute( 'data-trap', '1' );

    const content = this.getElement().querySelector( '.o-modal_content' );
    content.insertBefore( before, content.childNodes[0] );
    content.appendChild( after );
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
  handleClicks();
  handleEscKey();
  handleFocusChanges();
}

/**
 * Set up clicks to open (and close)
 */
function handleClicks() {
  document.addEventListener( 'click', event => {
    const t = event.target;
    const opener = t.closest( '[data-open-modal]' );
    if ( opener ) {
      event.preventDefault();
      event.stopPropagation();
      const id = opener.dataset.openModal;
      const modal = new Modal( id, opener );
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
}

/**
 * Allow closing via Esc key
 */
function handleEscKey() {
  document.addEventListener( 'keydown', event => {
    if ( event.key !== 'Escape' || !openModals.length ) {
      return;
    }

    openModals[openModals.length - 1].close();
    event.stopPropagation();
  } );
}

/**
 * Trap focus within the content
 */
function handleFocusChanges() {
  document.addEventListener( 'focusin', event => {
    const trap = event.target.closest( '[data-trap]' );
    if ( !trap ) {
      return;
    }

    const content = trap.closest( '.o-modal_content' );

    if ( trap.dataset.trap === '1' ) {
      const first = content.querySelector( '.o-modal_close' );
      first.focus();
    } else {
      // Try to focus the last button/link in footer
      const footer = content.querySelector( '.o-modal_footer' );
      const focusables = [].slice.call(
        footer.querySelectorAll( 'button,a[href]' )
      );
      focusables.reverse();
      if ( focusables.length ) {
        focusables[0].focus();
      }
    }
  } );
}

export { init, close };
