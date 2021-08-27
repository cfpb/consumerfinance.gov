export class TdpResultsPage {
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

  // stores shareUrl
  visitSharedUrl() {
    cy.get( '[data-open-modal="modal-share-url"]' ).click();
    cy.get( '#modal-share-url-initials-input' ).type( 'abcd{enter}' );
    cy.get( '.share-output button' ).click();

    cy.get( '.share-output a' ).then( a => {
      const url = a[0].href;

      cy.clearCookies();
      cy.visit( url );
    } );
  }

  checkInitials() {
    cy.get( '.initials-value' ).should( 'include.text', 'ABCD' );
  }

  checkNoSharing() {
    cy.get( '[data-open-modal="modal-share-url"]' ).should( 'not.exist' );
  }
}
