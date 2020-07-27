export class RuralOrUnderserved {

  open() {
    cy.visit( 'rural-or-underserved-tool/' );
  }

  searchAddress( address ) {
    this.addressForm().find( '#address1-input' ).type( '1600 Pennsylvania Avenue Washington DC' );
    this.addressForm().submit();
  }

  addressForm() {
    return cy.get( '#geocode' );
  }

  resultsTable() {
    return cy.get( '.rout-results-table' );
  }

}
