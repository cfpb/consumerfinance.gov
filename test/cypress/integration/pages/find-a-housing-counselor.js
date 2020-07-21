import { FindAHousingCounselor } from '../../pages/find-a-housing-counselor/find-a-housing-counselor';

const page = new FindAHousingCounselor();

describe('Find A Housing Counselor', () => {
  describe('Search Nearby', () => {
    it('should return nearby counselors', () => {
      page.open();
      page.searchZipCode('22204');
      page.resultsSection().should('be.visible');
    });
  });
});