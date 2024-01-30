import { jest } from '@jest/globals';
import actions from '../../../../../../cfgov/unprocessed/js/organisms/MortgagePerformanceTrends/actions/chart.js';

const mockAPIResponse = {
  getMetroData: {
    AL: {
      metros: [
        {
          valid: true,
          fips: '12345',
          name: 'Acme metro',
        },
        {
          valid: true,
          fips: '12-non',
          name: 'Acme non-metro',
        },
      ],
    },
  },
  getNonMetroData: [
    {
      valid: true,
      fips: '12345',
      name: 'Acme metro',
      abbr: 'AL',
    },
  ],
  getCountyData: {
    AL: {
      counties: [
        {
          valid: true,
          fips: '12345',
          name: 'Acme county',
        },
      ],
    },
  },
  getStateData: {
    10: {
      AP: 'Del.',
      fips: '10',
      name: 'Delaware',
      abbr: 'DE',
    },
    11: {
      AP: 'D.C.',
      fips: '11',
      name: 'District of Columbia',
      abbr: 'DC',
    },
  },
};

describe('Mortgage Performance chart action creators', () => {
  it('should dispatch actions to fetch metro states', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockAPIResponse.getMetroData),
      }),
    );

    let dispatch = jest.fn();
    await actions.fetchMetroStates('AL', true)(dispatch);
    expect(dispatch).toHaveBeenCalledTimes(2);
    dispatch = jest.fn();
    await actions.fetchMetroStates('CA', true)(dispatch);
    expect(dispatch).toHaveBeenCalledTimes(2);
  });

  it('should dispatch actions to fetch non-metro states', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockAPIResponse.getNonMetroData),
      }),
    );

    const dispatch = jest.fn();
    await actions.fetchNonMetroStates('WY', true)(dispatch);
    expect(dispatch).toHaveBeenCalledTimes(2);
  });

  it('should dispatch actions to fetch county states', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockAPIResponse.getCountyData),
      }),
    );

    const dispatch = jest.fn();
    await actions.fetchCountyStates('CA', true)(dispatch);
    expect(dispatch).toHaveBeenCalledTimes(2);
  });

  it('should dispatch actions to fetch states', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockAPIResponse.getStateData),
      }),
    );

    const dispatch = jest.fn();
    await actions.fetchStates('CA', true)(dispatch);
    expect(dispatch).toHaveBeenCalledTimes(3);
  });

  it('should dispatch actions to fetch metros', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockAPIResponse.getMetroData),
      }),
    );

    const dispatch = jest.fn();
    await actions.fetchMetros('AL', true)(dispatch);
    expect(dispatch).toHaveBeenCalledTimes(4);
    expect(actions.fetchMetros('AK', true)).toThrow();
  });

  it('should fail on bad metro state abbr', () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockAPIResponse.getMetroData),
      }),
    );

    expect(actions.fetchMetros('bloop', true)).toThrow();
  });

  it('should not require national data to be included with metros', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockAPIResponse.getMetroData),
      }),
    );

    const dispatch = jest.fn();
    await actions.fetchMetros('AL', false)(dispatch);
    expect(dispatch).toHaveBeenCalledTimes(4);
  });

  it('should dispatch actions to fetch counties', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockAPIResponse.getCountyData),
      }),
    );

    const dispatch = jest.fn();
    await actions.fetchCounties('AL', true)(dispatch);
    expect(dispatch).toHaveBeenCalledTimes(4);
  });

  it('should not require national data to be included with counties', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        json: () => Promise.resolve(mockAPIResponse.getCountyData),
      }),
    );

    const dispatch = jest.fn();
    await actions.fetchCounties('AL', false)(dispatch);
    expect(dispatch).toHaveBeenCalledTimes(4);
  });

  it('should fail on bad county state abbr', () => {
    expect(actions.fetchCounties('bloop', true)).toThrow();
  });
});
