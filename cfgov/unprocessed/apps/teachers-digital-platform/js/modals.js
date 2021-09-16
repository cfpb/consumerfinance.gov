const { closest } = require( '@cfpb/cfpb-atomic-component/src/utilities/dom-traverse.js' );
const CustomEvt = require( 'customevent' );

/**
 * Holds the only reference to Modal instance, which is only created just
 * before opened.
 */
let openModal = null;

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
    if ( openModal ) {
      openModal.close();
    }

    const el = this.getElement();

    const event = new CustomEvt( 'modal:open:before', {
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
    openModal = this;
  }

  close() {
    this.isOpen = false;
    openModal = null;

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
    if ( this.getElement().querySelector( '[data-trap]' ) ) {
      // Traps already created
      return;
    }

    const before = document.createElement( 'span' );
    before.tabIndex = 0;
    before.setAttribute( 'data-trap', '0' );
    before.setAttribute( 'aria-hidden', 'true' );
    const after = document.createElement( 'span' );
    after.tabIndex = 0;
    after.setAttribute( 'data-trap', '1' );
    after.setAttribute( 'aria-hidden', 'true' );

    const content = this.getElement().querySelector( '.o-modal_content' );
    content.insertBefore( before, content.childNodes[0] );
    content.appendChild( after );
  }
}

/**
 * Close the modal
 */
function close() {
  if ( openModal ) {
    openModal.close();
  }
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
    const opener = closest( t, '[data-open-modal]' );
    if ( opener ) {
      event.preventDefault();
      event.stopPropagation();
      const id = opener.dataset.openModal;
      const modal = new Modal( id, opener );
      modal.open();
      return;
    }

    if ( !openModal ) {
      return;
    }

    const closeAndCancelEvent = () => {
      openModal.close();
      event.stopPropagation();
    };

    const content = openModal.getElement().querySelector( '.o-modal_content' );
    if ( content.contains( t ) ) {
      // Close if clicking modal's close button(s)
      if ( content.querySelector( '.o-modal_close' ).contains( t ) ) {
        closeAndCancelEvent();
        return;
      }

      // Close if clicked footer button with "close"
      const btn = content.querySelector( '.o-modal_footer button' );
      if ( t === btn && ( /\bclose\b/i ).test( btn.textContent ) ) {
        closeAndCancelEvent();
      }
    } else {
      // Outside modal
      closeAndCancelEvent();
    }
  } );
}

/**
 * Allow closing via Esc key
 */
function handleEscKey() {
  document.addEventListener( 'keydown', event => {
    if ( event.key !== 'Escape' || !openModal ) {
      return;
    }

    openModal.close();
    event.stopPropagation();
  } );
}

/**
 * Trap focus within the content
 */
function handleFocusChanges() {
  document.addEventListener( 'focusin', event => {
    const trap = closest( event.target, '[data-trap]' );
    if ( !trap ) {
      return;
    }

    const content = closest( trap, '.o-modal_content' );

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
