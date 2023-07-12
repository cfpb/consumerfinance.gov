const config = {
  rateCheckerAPI: '/oah-api/rates/rate-checker',
  countyAPI: '/oah-api/county/',
};

/**
 * Get data from the API.
 * @param {object} fieldToFetch - Hash of fields to add to the query.
 * @returns {Promise} A promise for the request.
 */
function getData(fieldToFetch) {
  const controller = new AbortController();
  const { signal } = controller;

  return {
    promise: fetch(
      `${config.rateCheckerAPI}?${new URLSearchParams(fieldToFetch)}`,
      { signal },
    ),
    controller,
  };
}

/**
 * Get a list of counties from the API for the selected state.
 * @param {string} state - The state to get counties for.
 * @returns {Promise} A promise for the request.
 */
function getCounties(state) {
  return fetch(`${config.countyAPI}?${new URLSearchParams({ state })}`).then(
    (res) => res.json(),
  );
}

export { getData, getCounties };
