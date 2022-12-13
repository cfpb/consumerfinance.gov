import fetchMock from 'jest-fetch-mock';
fetchMock.enableMocks();
import { jest } from '@jest/globals';
import defaultActionCreators from '../../../../../../cfgov/unprocessed/js/organisms/MortgagePerformanceTrends/actions/default.js';

jest.unstable_mockModule(
  '../../../../../../cfgov/unprocessed/js/organisms/MortgagePerformanceTrends/utils.js',
  () => ({
    getNonMetroData: (cb) => {
      const nonMetros = [
        {
          valid: true,
          fips: '12345',
          name: 'Acme metro',
          abbr: 'AL',
        },
      ];
      cb(nonMetros);
    },
  })
);

xdescribe('Mortgage Performance default action creators', () => {
  it('should create an action to set a geo', () => {
    const action = defaultActionCreators().setGeo(12345, 'Alabama', 'state');
    expect(action).toStrictEqual({
      type: 'SET_GEO',
      geo: {
        type: 'state',
        id: 12345,
        name: 'Alabama',
      },
    });
  });

  it('should create an action to clear geos', () => {
    const action = defaultActionCreators().clearGeo();
    expect(action).toStrictEqual({
      type: 'CLEAR_GEO',
    });
  });

  it('should create actions to update charts', () => {
    let action = defaultActionCreators().updateChart(
      12345,
      'Alabama',
      'state',
      false
    );
    expect(action).toStrictEqual({
      type: 'UPDATE_CHART',
      geo: {
        type: 'state',
        id: 12345,
        name: 'Alabama',
      },
      includeComparison: false,
    });
    action = defaultActionCreators().updateChart(null, null, null, false);
    expect(action).toStrictEqual({
      type: 'UPDATE_CHART',
      geo: {
        id: null,
        name: null,
      },
      includeComparison: false,
    });
  });

  it('should create an action to update the national comparison', () => {
    const action = defaultActionCreators().updateNational(false);
    expect(action).toStrictEqual({
      type: 'UPDATE_CHART',
      includeComparison: false,
    });
  });

  it('should create an action to update the date', () => {
    const action = defaultActionCreators().updateDate('2010-01');
    expect(action).toStrictEqual({
      type: 'UPDATE_DATE',
      date: '2010-01',
    });
  });

  it('should create an action to request counties', () => {
    const action = defaultActionCreators().requestCounties();
    expect(action).toStrictEqual({
      type: 'REQUEST_COUNTIES',
      isLoadingCounties: true,
    });
  });

  it('should create an action to request metros', () => {
    const action = defaultActionCreators().requestMetros();
    expect(action).toStrictEqual({
      type: 'REQUEST_METROS',
      isLoadingMetros: true,
    });
  });

  it('should create an action to request non-metros', () => {
    const action = defaultActionCreators().requestNonMetros();
    expect(action).toStrictEqual({
      type: 'REQUEST_NON_METROS',
      isLoadingNonMetros: true,
    });
  });

  it('should dispatch actions to fetch non-metros', () => {
    const dispatch = jest.fn();
    defaultActionCreators().fetchNonMetros('AL', true)(dispatch);
    expect(dispatch).toHaveBeenCalledTimes(4);
    defaultActionCreators().fetchNonMetros('CA', true)(dispatch);
    expect(dispatch).toHaveBeenCalledTimes(8);
  });

  it('should fail on bad non-metro state abbr', () => {
    expect(defaultActionCreators().fetchNonMetros('bloop', true)).toThrow();
  });

  it('should create an action to set metros', () => {
    const action = defaultActionCreators().setMetros([{ name: 'Akron, OH' }]);
    expect(action).toStrictEqual({
      type: 'SET_METROS',
      metros: [{ name: 'Akron, OH' }],
    });
  });

  it('should create an action to set non-metros', () => {
    const action = defaultActionCreators().setNonMetros([
      { name: 'Tampa, FL' },
    ]);
    expect(action).toStrictEqual({
      type: 'SET_NON_METROS',
      nonMetros: [{ name: 'Tampa, FL' }],
    });
  });

  it('should create an action to set counties', () => {
    const action = defaultActionCreators().setCounties([
      { name: 'Acme County' },
    ]);
    expect(action).toStrictEqual({
      type: 'SET_COUNTIES',
      counties: [{ name: 'Acme County' }],
    });
  });

  it('should create an action to start loading', () => {
    const action = defaultActionCreators().startLoading();
    expect(action).toStrictEqual({
      type: 'START_LOADING',
      isLoading: true,
    });
  });

  it('should create an action to stop loading', () => {
    const action = defaultActionCreators().stopLoading();
    expect(action).toStrictEqual({
      type: 'STOP_LOADING',
      isLoading: false,
    });
  });
});
