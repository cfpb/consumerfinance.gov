import { convertDate } from './calculation';
import getTileMapColor from './get-tile-map-color';
import getTileMapState from './get-tile-map-state';

let UNDEFINED;

/**
 * Prepares mortgage delinquency data for Highcharts.
 * @param {number} datasets - Raw JSON from mortgage-performance API.
 * @returns {object} datasets - Nested array.
 */
function processDelinquencies(datasets) {
  if (typeof datasets !== 'object') {
    return datasets;
  }

  if (!datasets[0].data[0].value) {
    return 'propertyError';
  }

  datasets = datasets.map((dataset) => ({
    label: dataset.meta.name,
    data: dataset.data.map((datum) => [datum.date, datum.value]),
  }));

  return datasets;
}

/**
 * @param {number} data - response from requested JSON file.
 * @param {string} [group] -
 *   Optional parameter for specifying if the chart requires use of a "group"
 *   property in the JSON, for example the charts with a group of "Younger
 *   than 30" will filter data to only include values matching that group.
 * @param {string} [source] -
 *   Optional parameter for the file url and name. Used for inquiry index files
 *   which have 4 months of projected data instead of 6.
 * @returns {object} data -
 *   Object with adjusted and unadjusted value arrays containing timestamps
 *   and a number value.
 */
function processNumOriginationsData(data, group, source) {
  if (typeof data !== 'object') {
    return data;
  }

  // check for data integrity!
  if (group !== null && Object.hasOwn(data, group)) {
    data = data[group];
  } else if (group !== null && !Object.hasOwn(data, group)) {
    // If group is not a property of the data, return an error
    return 'groupError';
  }
  // if data does not have correct properties, return an error
  if (!Object.hasOwn(data, 'adjusted') || !Object.hasOwn(data, 'unadjusted')) {
    return 'propertyError';
  }

  data.unadjusted = data.unadjusted.sort(function (a, b) {
    return a[0] - b[0];
  });
  data.adjusted = data.adjusted.sort(function (a, b) {
    return a[0] - b[0];
  });

  data.projectedDate = {};
  let projectedMonths = 6;
  // set number of months of projected data based on whether source filename includes 'inq' or 'crt' for inquiries or credit tightness
  if (source && source.indexOf('inq_') !== -1) {
    projectedMonths = 4;
  } else if (source && source.indexOf('crt_') !== -1) {
    projectedMonths = 0;
  }
  data.projectedDate.timestamp = getProjectedTimestamp(
    data.adjusted,
    projectedMonths,
  );
  data.projectedDate.label = getProjectedDate(data.projectedDate.timestamp);

  return data;
}

/**
 * @param {number} data - response from requested JSON file.
 * @param {string} [group] -
 *   Optional parameter for specifying if the chart requires use of a "group"
 *   property in the JSON, for example the charts with a group of "Younger
 *   than 30" will filter data to only include values matching that group.
 * @returns {object} data -
 *   Object with adjusted and unadjusted value arrays containing timestamps
 *   and a number value.
 */
function processYoyData(data, group) {
  if (typeof data !== 'object') {
    return data;
  }

  // check for data integrity!
  if (group !== null && Object.hasOwn(data, group)) {
    data = data[group];
  } else if (group !== null && !Object.hasOwn(data, group)) {
    // If group is not a property of the data, return an error
    return 'groupError';
  }

  data.projectedDate = {};
  data.projectedDate.timestamp = getProjectedTimestamp(data, 6);
  data.projectedDate.label = getProjectedDate(data.projectedDate.timestamp);

  return data;
}

/**
 * Returns a UTC timestamp number for the month
 * when each graph's data is projected.
 *
 * For Mortgage Performance Trends data, there is no projected data.
 * For Consumer Credit Trends data, projected data is for the last 6 months,
 * except for inquiry index data, which is for the last 4 months, and credit
 * tightness index data, which has no projected data.
 * @param {Array} valuesList -
 *   List of values from the data, containing an array with timestamp
 *   representing the month and year at index 0, and the value at index 1.
 *   Requires at least six months of data (six array items).
 * @param {string} projectedRange -
 *   Number of months in the data that is to be labeled projected.
 *   The default is 6 months, inquiry index charts are 4 months, etc.
 * @returns {number} A timestamp.
 */
function getProjectedTimestamp(valuesList, projectedRange = 6) {
  if (projectedRange === 0) {
    return UNDEFINED;
  }

  const projectedMonth = valuesList[valuesList.length - projectedRange][0];

  return convertDate(projectedMonth).timestamp;
}

/**
 * Returns a human-readable string representing the month and year after,
 * which data in each graph is projected.
 * @param {number} timestamp -
 *   UTC timestamp representing the milliseconds elapsed since the UNIX epoch,
 *   for the month when each graph begins displaying projected data.
 * @returns {string}
 *   projectedDate - text with the Month and Year of the projected data cutoff
 *   point, for use in labeling projected date in graphs.
 */
function getProjectedDate(timestamp) {
  const getDate = new Date(timestamp);
  getDate.setUTCMonth(getDate.getUTCMonth() - 1);
  const projectedDate = convertDate(getDate.getTime()).humanFriendly;

  return projectedDate;
}

/**
 * @param {object} data - Data to process.
 * @returns {object} The processed data.
 */
function processMapData(data) {
  if (typeof data !== 'object') {
    return data;
  }

  // Filter out any empty values just in case
  data = data.filter(function (row) {
    return Boolean(row.name);
  });

  data = data.map(function (obj) {
    const state = getTileMapState[obj.name];
    const value = Math.round(obj.value);
    const tooltip =
      state.abbr +
      ' ' +
      (value < 0 ? 'decreased' : 'increased') +
      ' by ' +
      Math.abs(value) +
      '%';
    return {
      name: obj.name,
      path: state.path,
      value: value,
      tooltip: tooltip,
      color: getTileMapColor.getColorByValue(value),
    };
  });

  return data;
}

export {
  processDelinquencies,
  processNumOriginationsData,
  processYoyData,
  processMapData,
  getProjectedDate,
  getProjectedTimestamp,
};
