import mapboxAPIResponses from '../../../fixtures/mapbox-api.json';

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
        request.reply(mapboxAPIResponses.streets);
      }
    ).as('mapboxStreets');
    cy.intercept(
      {
        url: /api\.mapbox\.com\/v\d+/,
      },
      (request) => {
        request.reply(mapboxAPIResponses.text);
      }
    ).as('mapboxText');
  }

  searchZipCode(zipCode) {
    cy.get('#hud_hca_api_query').type(zipCode);
    cy.get('[data-cy=btn-fahc-submit]').click();
  }

  resultsSection() {
    return cy.get('#hud_results-list_container');
  }
}
