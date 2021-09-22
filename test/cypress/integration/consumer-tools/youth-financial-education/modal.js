const URL = '/consumer-tools/educator-tools/youth-financial-education/survey/3-5/';

function open() {
  cy.get( '[data-open-modal="modal-privacy"]' ).click();
  cy.get( '#modal-privacy .o-modal_body' ).should( 'be.visible' );
}
function checkClosed() {
  cy.get( '#modal-privacy .o-modal_body' ).should( 'be.hidden' );
}

describe( 'Youth Financial Education Survey: modal', () => {
  it( 'can be opened', () => {
    cy.visit( URL );

    cy.get( '#modal-privacy' ).then( $el => {
      expect( $el.attr( 'role' ) ).equal( 'alertdialog' );
    } );

    cy.get( '#modal-privacy .o-modal_body' ).should( 'be.hidden' );
    cy.get( '#modal-privacy' ).then( $el => {
      expect( $el.attr( 'aria-hidden' ) ).equal( 'true' );
      expect( $el.attr( 'aria-modal' ) ).to.be.undefined;
    } );
    open();
    cy.get( '#modal-privacy' ).then( $el => {
      expect( $el.attr( 'aria-hidden' ) ).equal( 'false' );
      expect( $el.attr( 'aria-modal' ) ).equal( 'true' );
    } );
  } );

  it( 'traps focus', () => {
    cy.visit( URL );
    cy.get( '[data-open-modal="modal-privacy"]' ).click();

    cy.get( '#modal-privacy [data-trap="1"]' )
      .should( 'be.hidden' )
      .focus();

    cy.get( 'button.o-modal_close' ).should( 'have.focus' );

    cy.get( '#modal-privacy [data-trap="0"]' )
      .should( 'be.hidden' )
      .focus();

    cy.get( '.o-modal_footer button' ).should( 'have.focus' );
  } );

  it( 'can close 4 ways', () => {
    cy.visit( URL );

    open();
    cy.get( '.o-modal_body .o-modal_close' ).click();
    checkClosed();

    open();
    cy.get( '.o-modal_footer button' ).click();
    checkClosed();

    open();
    cy.get( '.o-modal_container' ).click( 'topRight' );
    checkClosed();

    open();
    cy.get( '.o-modal_container' ).trigger( 'keydown', { keyCode: 27, key: 'Escape' } );
    checkClosed();
  } );

  it( 'does not close when content clicked', () => {
    cy.visit( URL );

    open();
    cy.get( '#modal-privacy_desc' ).click();
    cy.get( '#modal-privacy .o-modal_body' ).should( 'be.visible' );
  } );
} );
