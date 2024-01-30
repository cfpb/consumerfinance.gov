import { jest } from '@jest/globals';
import actions from '../../../../../../cfgov/unprocessed/js/organisms/MortgagePerformanceTrends/actions/map.js';

const mockAPIResponse = {
  getMetroData: () => {
    return {
      AL: {
        metros: [
          {
            valid: true,
            fips: '12345',
            name: 'Acme metro',
          },
        ],
      },
    };
  },
  getCountyData: () => {
    return {
      AL: {
        counties: [
          {
            valid: true,
            fips: '12345',
            name: 'Acme county',
          },
        ],
      },
    };
  },
};

describe('Mortgage Performance map action creators', () => {
  it('should create an action to update the chart', () => {
    const action = actions.updateChart(123, 'Alabama', 'state');
    expect(action).toStrictEqual({
      type: 'UPDATE_CHART',
      geo: {
        id: 123,
        name: 'Alabama',
        type: 'state',
      },
    });
  });

  it('should create an action without a geo type', () => {
    const action = actions.updateChart(123, 'Alabama');
    expect(action).toStrictEqual({
      type: 'UPDATE_CHART',
      geo: {
        id: 123,
        name: 'Alabama',
      },
    });
  });

  it('should create an action without a geoId', () => {
    const action = actions.updateChart(null, null);
    expect(action).toStrictEqual({
      type: 'UPDATE_CHART',
      geo: {
        id: null,
        name: null,
      },
      counties: [],
      metros: [],
    });
  });

  describe('getMetroData', () => {
    beforeEach(() => {
      global.fetch = jest.fn(() =>
        Promise.resolve({
          json: () => Promise.resolve(mockAPIResponse.getMetroData()),
        }),
      );
    });

    xit('should dispatch actions to fetch metros', async () => {
      const dispatch = jest.fn();
      await actions.fetchMetros('AL', true)(dispatch);
      expect(dispatch).toHaveBeenCalledTimes(3);
    });

    it('should fail on bad metro state abbr', () => {
      expect(actions.fetchMetros('bloop', true)).toThrow();
    });

    it('should not require map zoom after fetching metros', async () => {
      const dispatch = jest.fn();
      await actions.fetchMetros('AL', false)(dispatch);
      expect(dispatch).toHaveBeenCalledTimes(2);
    });
  });

  describe('getCountyData', () => {
    beforeEach(() => {
      global.fetch = jest.fn(() =>
        Promise.resolve({
          json: () => Promise.resolve(mockAPIResponse.getCountyData()),
        }),
      );
    });

    it('should dispatch actions to fetch counties', async () => {
      const dispatch = jest.fn();
      await actions.fetchCounties('AL', true)(dispatch);
      expect(dispatch).toHaveBeenCalledTimes(3);
    });

    xit('should not require map zoom after fetching counties', async () => {
      const dispatch = jest.fn();
      await actions.fetchCounties('AL', false)(dispatch);
      expect(dispatch).toHaveBeenCalledTimes(2);
    });

    it('should fail on bad county state abbr', () => {
      expect(actions.fetchCounties('bloop', true)).toThrow();
    });
  });
});
