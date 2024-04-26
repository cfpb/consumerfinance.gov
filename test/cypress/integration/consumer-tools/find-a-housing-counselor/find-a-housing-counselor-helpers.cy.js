import responseMapboxAPIStreets from '../../../fixtures/fahc-mapbox-api-streets.json';
import responseMapboxAPIText from '../../../fixtures/fahc-mapbox-api-text.json';

export class FindAHousingCounselor {
  open() {
    cy.visit('/find-a-housing-counselor/');
  }

  // Stub Mapbox API responses
  interceptMapboxAPIRequests() {
    cy.intercept(
      {
        url: /api\.mapbox\.com\/styles\/v1\/mapbox\/streets-v\d+\?access_token/,
      },
      (request) => {
        request.reply(responseMapboxAPIStreets);
      },
    ).as('mapboxStreets');
    cy.intercept(
      {
        url: /api\.mapbox\.com\/v\d+/,
      },
      (request) => {
        request.reply(responseMapboxAPIText);
      },
    ).as('mapboxText');
  }

  searchZipCode(zipCode) {
    cy.get('#hud-hca-api-query').type(zipCode);
    cy.get('[data-cy=btn-fahc-submit]').click();
  }

  resultsSection() {
    return cy.get('#hud_results-list_container');
  }
}
