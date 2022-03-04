import censusAPIResponses from '../../../fixtures/census-api.json';

export class RuralOrUnderservedTool {

  open() {
    cy.visit( 'rural-or-underserved-tool/' );
  }

  searchAddress( address ) {
    this.addressForm().find( '#address1-input' ).type( `${ address }` );
    this.addressForm().submit();
  }

  addressForm() {
    return cy.get( '#geocode' );
  }

  resultsTable() {
    return cy.get( '.rout-results-table' );
  }

  // Stub Census API responses so tests don't fail if their API is slow
  interceptCensusAPIRequests() {
    cy.intercept( {
      url: /geocoding\.geo\.census\.gov/
    },
    request => { request.reply( censusAPIResponses.geocoding ); } )
      .as( 'censusGeocoding' );
    cy.intercept( {
      url: /tigerweb\.geo\.census\.gov/,
      query: {
        callback: '__jp1'
      }
    },
    request => { request.reply( censusAPIResponses.tigerweb1 ); } )
      .as( 'censusTigerweb1' );
    cy.intercept( {
      url: /tigerweb\.geo\.census\.gov/,
      query: {
        callback: '__jp2'
      }
    },
    request => { request.reply( censusAPIResponses.tigerweb2 ); } )
      .as( 'censusTigerweb2' );
    cy.intercept( {
      url: /tigerweb\.geo\.census\.gov/,
      query: {
        callback: '__jp3'
      }
    },
    request => { request.reply( censusAPIResponses.tigerweb3 ); } )
      .as( 'censusTigerweb3' );
  }

}
