import { checkHudData } from '../../../../../cfgov/unprocessed/apps/find-a-housing-counselor/js/hud-util';

describe('hud', () => {
  describe('checkHudData', () => {
    it('Should return true on a valid HUD data, false otherwise.', () => {
      const mockData = {
        // eslint-disable-next-line camelcase
        counseling_agencies: [{}],
        zip: {},
      };
      expect(checkHudData(mockData)).toBe(true);
      expect(checkHudData('')).toBe(false);
      expect(checkHudData(null)).toBe(false);
    });
  });
});
