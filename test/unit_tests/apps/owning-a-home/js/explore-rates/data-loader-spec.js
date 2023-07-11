import { jest } from '@jest/globals';
import {
  getData,
  getCounties,
} from '../../../../../../cfgov/unprocessed/apps/owning-a-home/js/explore-rates/data-loader.js';

const mockResp = { data: 'mock data' };

global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve(mockResp),
  }),
);

describe('explore-rates/data-loader', () => {
  describe('getData()', () => {
    it('should call data API with correct query', () => {
      getData({ a: 'b', c: 'd' });
      return expect(fetch.mock.calls[0][0]).toBe(
        '/oah-api/rates/rate-checker?a=b&c=d',
      );
    });
  });

  describe('getCounties()', () => {
    it('should call county API with correct state query', () => {
      getCounties('AL');
      return expect(fetch).toHaveBeenCalledWith('/oah-api/county/?state=AL');
    });
  });
});
