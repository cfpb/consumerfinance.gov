import defaultActionCreators from './default';
import utils from '../utils';

const mapActionCreators = defaultActionCreators();

/**
 * zoomChart - Creates action to zoom chart
 * @param {string} stateAbbr - Two-letter U.S. state abbreviation.
 * @returns {object} zoom chart action
 */
mapActionCreators.zoomChart = (stateAbbr) => {
  const action = {
    type: 'ZOOM_CHART',
    target: stateAbbr,
  };
  return action;
};

/**
 * updateChart - Creates action to re-render chart
 * @param {string} geoId - ID of location
 * @param {string} geoName - Name of location
 * @param {string} geoType - Type of location (state, metro, county)
 * @returns {object} update chart action
 */
mapActionCreators.updateChart = (geoId, geoName, geoType) => {
  const action = {
    type: 'UPDATE_CHART',
    geo: {
      id: geoId,
      name: geoName,
    },
  };
  if (geoType) {
    action.geo.type = geoType;
  }
  if (!geoId) {
    action.counties = [];
    action.metros = [];
  }
  return action;
};

/**
 * fetchMetros - Creates async action to fetch list of metros
 * @param {string} metroState - Two-letter U.S. state abbreviation.
 * @param {boolean} shouldZoom - Zoom to U.S. state after fetching?
 * @returns {Function} Thunk called with new metros
 */
mapActionCreators.fetchMetros = (metroState, shouldZoom) => (dispatch) => {
  dispatch(mapActionCreators.requestMetros(metroState));
  return utils.getMetroData((data) => {
    // Alphabetical order
    let newMetros = data[metroState].metros.sort((a, b) =>
      a.name < b.name ? -1 : 1,
    );
    newMetros = newMetros.filter((metro) => metro.valid);
    if (!newMetros.length) {
      newMetros = [
        {
          fips: null,
          name: 'No metros have sufficient data',
        },
      ];
    }
    dispatch(mapActionCreators.setMetros(newMetros));
    if (newMetros.length && shouldZoom) {
      dispatch(mapActionCreators.zoomChart(metroState));
    }
    return newMetros;
  });
};

/**
 * fetchCounties - Creates async action to fetch list of counties
 * @param {string} countyState - Two-letter U.S. state abbreviation.
 * @param {boolean} shouldZoom - Zoom to U.S. state after fetching?
 * @returns {Function} Thunk called with new metros
 */
mapActionCreators.fetchCounties = (countyState, shouldZoom) => (dispatch) => {
  dispatch(mapActionCreators.requestCounties(countyState));
  return utils.getCountyData((data) => {
    // Alphabetical order
    let newCounties = data[countyState].counties.sort((a, b) =>
      a.name < b.name ? -1 : 1,
    );
    newCounties = newCounties.filter((county) => county.valid);
    dispatch(mapActionCreators.setCounties(newCounties));
    if (newCounties.length && shouldZoom) {
      dispatch(mapActionCreators.zoomChart(countyState));
    }
    return newCounties;
  });
};

export default mapActionCreators;
