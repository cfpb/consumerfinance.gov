import * as modals from '../../../../../cfgov/unprocessed/apps/teachers-digital-platform/js/modals';
import HTML_SNIPPET from '../html/survey-page';

const $ = document.querySelector.bind( document );

describe( 'TDP modals', () => {
  let modal;
  let opener;

  beforeEach( () => {
    document.body.innerHTML = HTML_SNIPPET;

    modal = $( '#modal-restart' );
    opener = $( '[data-open-modal="modal-restart"]' );
  } );

  beforeAll( () => {
    modals.init();
  } );

  it( 'opens on clicking elements with [data-open-modal]', () => {
    expect( modal.getAttribute( 'aria-hidden' ) ).toEqual( 'true' );
    opener.click();
    expect( modal.getAttribute( 'aria-hidden' ) ).toEqual( 'false' );
  } );

  it( 'closes on clicking outside/close buttons/esc key', () => {
    const open = () => {
      opener.click();
      expect( modal.getAttribute( 'aria-hidden' ) ).toEqual( 'false' );
    };
    const verifyClosed = () => {
      expect( modal.getAttribute( 'aria-hidden' ) ).toEqual( 'true' );
    };

    open();

    $( 'label[for="id_p1-q6_1"]' ).click();
    verifyClosed();

    open();

    modal.querySelector( '.o-modal_close' ).click();
    verifyClosed();

    open();

    // This shouldn't work
    document.dispatchEvent( new KeyboardEvent( 'keydown', { key: 'A' } ) );
    expect( modal.getAttribute( 'aria-hidden' ) ).toEqual( 'false' );

    // This does
    document.dispatchEvent( new KeyboardEvent( 'keydown', { key: 'Escape' } ) );
    verifyClosed();

    open();

    modal.querySelector( '.o-modal_footer button' ).click();
    verifyClosed();

    open();

    modals.close();
    verifyClosed();
  } );

  it( 'traps focus', () => {
    const firstClose = modal.querySelector( '.o-modal_close' );
    const lastButton = modal.querySelector( '[data-cancel="1"]' );
    const closeFocusSpy = jest.spyOn( firstClose, 'focus' );
    const lastButtonFocusSpy = jest.spyOn( lastButton, 'focus' );

    let evt = new FocusEvent( 'focusin' );
    jest.spyOn( evt, 'target', 'get' ).mockImplementation(
      () => modal.querySelector( '[data-trap="0"]' )
    );
    document.dispatchEvent( evt );
    expect( lastButtonFocusSpy ).toHaveBeenCalled();

    evt = new FocusEvent( 'focusin' );
    jest.spyOn( evt, 'target', 'get' ).mockImplementation(
      () => modal.querySelector( '[data-trap="1"]' )
    );
    document.dispatchEvent( evt );
    expect( closeFocusSpy ).toHaveBeenCalled();

    expect( lastButtonFocusSpy.mock.calls.length ).toEqual( 1 );
    expect( closeFocusSpy.mock.calls.length ).toEqual( 1 );
    document.body.dispatchEvent( new Event( 'focusin' ) );
    expect( lastButtonFocusSpy.mock.calls.length ).toEqual( 1 );
    expect( closeFocusSpy.mock.calls.length ).toEqual( 1 );
  } );
} );
