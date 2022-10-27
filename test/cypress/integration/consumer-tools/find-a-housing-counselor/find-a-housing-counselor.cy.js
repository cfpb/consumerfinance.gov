import { FindAHousingCounselor } from './find-a-housing-counselor-helpers.cy.js';

const page = new FindAHousingCounselor();

describe('Find a housing counselor', () => {
  describe('Search by ZIP code', () => {
    beforeEach(() => {
      // Return a fixture for the Mapbox APIs for the ZIP code 22204
      page.interceptMapboxAPIRequests();
    });

    it('should return nearby counselors', () => {
      page.open();
      page.searchZipCode('22204');
      cy.wait(['@mapboxStreets', '@mapboxText']);
      page.resultsSection().should('be.visible');
    });
  });
});
