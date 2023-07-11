import {
  benefits,
  lifetime,
  fetchApiData,
  updateDataFromApi,
} from '../../../../../../cfgov/unprocessed/apps/retirement/js/data';
import { r1, r2, r3 } from './responses.js';
import fetchMock from 'jest-fetch-mock';

fetchMock.enableMocks();

describe('fetchApiData', function () {
  it('fetches data', function () {
    fetch.mockResponseOnce(JSON.stringify({ data: '12345' }));
    fetchApiData('11-11-1965', 34567).then(
      (res) => {
        expect(res.data).toEqual('12345');
      },
      () => {
        throw new Error('It should not reject a valid call');
      },
    );
  });
  it('throws on bad data types', function () {
    expect(() => fetchApiData(Date.now(), '$34567')).toThrow();
  });
});

describe('updateDataFromApi', function () {
  it('updates data after an API call', function () {
    updateDataFromApi(r1);
    expect(benefits.fullAge).toEqual(67);
    expect(benefits.currentAge).toEqual(62);
    expect(lifetime.age62).toEqual(251217);
  });

  it('sets fullAge to current age if user is older', function () {
    updateDataFromApi(r2);
    expect(benefits.fullAge).toEqual(68);
    expect(benefits.currentAge).toEqual(68);
    expect(lifetime.age70).toEqual(295920);
  });

  it('sets fullAge and earlyAge appropriately if given non-Numeric response', function () {
    updateDataFromApi(r3);
    expect(benefits.fullAge).toEqual(67);
    expect(benefits.currentAge).toEqual(67);
    expect(lifetime.age70).toEqual(299520);
  });
});
