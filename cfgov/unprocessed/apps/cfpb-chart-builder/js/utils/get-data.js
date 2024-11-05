import cache from './session-storage';

let DATA_SOURCE_BASE = 'https://files.consumerfinance.gov/data/';

const getData = (sources) => {
  // Let browsers override the data source root (useful for localhost testing).
  DATA_SOURCE_BASE = window.CFPB_CHART_DATA_SOURCE_BASE || DATA_SOURCE_BASE;

  const urls = sources.split(';');

  const promises = urls.map((url) => {
    // Only prepend the data source base if it's a relative URL.
    if (url.indexOf('http') !== 0 && url.indexOf('/') !== 0) {
      url = DATA_SOURCE_BASE + url.replace('.csv', '.json');
    }

    if (cache.getItem(url)) {
      return Promise.resolve(cache.getItem(url));
    }

    return fetch(url).then((resp) => {
      return resp.json().then((data) => {
        cache.setItem(url, data);
        return data;
      });
    });
  });

  return Promise.all(promises);
};

export default getData;
