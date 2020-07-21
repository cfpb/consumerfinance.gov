export class FindAHousingCounselor {
  open() {
    cy.visit( '/find-a-housing-counselor/' );
  }

  searchZipCode( zipCode ) {
    cy.get( '#hud_hca_api_query' ).type( zipCode );
    cy.get( '.m-form-field-with-button_wrapper' ).within( () => {
      cy.get( 'button' ).click();
    } );
  }

  resultsSection() {
    return cy.get( '#hud_results-list_container' );
  }
}
