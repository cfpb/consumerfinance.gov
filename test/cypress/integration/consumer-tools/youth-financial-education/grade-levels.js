describe( 'Youth Financial Education Survey: Grade Selection', () => {
  for ( const grades of [ '3-5', '6-8', '9-12' ] ) {
    it( `Can load ${ grades } page`, () => {
      cy.visit( `/consumer-tools/educator-tools/youth-financial-education/survey/${ grades }/` );
    } );

    it( `${ grades } page has heading`, () => {
      cy.get( '.m-hero_text' ).should( 'include.text', `Grades ${ grades }` );
    } );

    it( `${ grades } page has start link`, () => {
      cy.get( '.survey-entry-link' ).should( 'have.attr', 'href', 'p1/' );
    } );

    it( `${ grades } page has privacy modal`, () => {
      cy.get( '[data-open-modal="modal-privacy"]' ).click();

      cy.get( '#modal-privacy_title' )
        .should( 'be.visible' )
        .should( 'include.text', 'Privacy Notice' );
    } );
  }
} );
