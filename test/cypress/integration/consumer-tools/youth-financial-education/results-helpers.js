export class TdpResultsHelpers {
  getPath( grades ) {
    return `/consumer-tools/educator-tools/youth-financial-education/survey/${ grades }/results/`;
  }

  checkStudentCookies( resultUrlPattern ) {
    cy.getCookie( 'wizard_survey_wizard' ).should( 'not.exist' );
    cy.getCookie( 'resultUrl' )
      .then( cookie => {
        expect( cookie.value ).to.match( resultUrlPattern );
      } );
  }

  checkCarPositions( xValues ) {
    cy.get( 'svg image' )
      .then( images => {
        xValues.forEach( ( val, idx ) => {
          expect( images[idx].getAttribute( 'x' ) ).to.equal( String( val ) );
        } );
      } );
  }

  print() {
    cy.get( '[data-open-modal="modal-print"]' ).click();

    cy.window().then( win => {
      cy.stub( win, 'print' ).returns( true );
    } );
    cy.get( '#modal-print-initials-input' ).type( 'abcd{enter}' );
    cy.window().then( win => {
      expect( win.print ).to.be.calledOnce;
    } );

    cy.get( '.initials-value' ).should( 'include.text', 'ABCD' );
  }

  visitSharedUrl() {
    cy.get( '[data-open-modal="modal-share-url"]' ).click();
    cy.get( '#modal-share-url-initials-input' ).should( 'have.value', 'ABCD' );

    cy.get( '#modal-share-url .tdp-survey__initials-set' ).click();

    cy.get( '.share-output a' ).then( a => {
      const url = a[0].href;

      cy.clearCookies();
      cy.visit( url );
    } );
  }

  checkInitials() {
    cy.get( '.initials-value' )
      .should( 'include.text', 'ABCD' )
      .should( 'be.hidden' );
  }

  checkDifferentInitials() {
    /**
     * Since ?r= values are server-keyed, we have to test with a URL generated
     * on this site, we just re-use the one we're on.
     */
    cy.url().then( url => {
      const newUrl = url.replace( /#.*/, '#==Vld4V1lWTkJQVDA9' );
      cy.visit( newUrl );
      // As usual, browsers are bad at picking up hash changes until reload.
      cy.reload();
      cy.get( '.initials-value' ).should( 'include.text', 'EFG' );
    } );
  }

  checkNoSharing() {
    cy.get( '[data-open-modal="modal-share-url"]' ).should( 'not.exist' );
  }
}
