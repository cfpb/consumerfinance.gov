import chartHooks from './chart-hooks.js';
import { extractSeries, overrideStyles } from './utils.js';

/**
 * Generates an array of filters, bucketed based on key if present
 * @param {object} filter - Object with a filter key and possible label
 * @param {object} data - The raw chart data
 * @param {boolean} isDate - Whether the data should be stored as JS dates
 * @returns {Array} All the buckets of data
 */
function getDataBuckets(filter, data, isDate) {
  const vals = {};
  const key = filter.key ? filter.key : filter;
  data.forEach((d) => {
    let item = d[key];
    if (!Array.isArray(item)) item = [item];
    item.forEach((v) => {
      vals[v] = 1;
    });
  });

  const options = Object.keys(vals);
  if (isDate) return options.map((v) => Number(new Date(v)));
  return options;
}

/**
 * @param {number} option - The JS-date formatted option
 * @returns {string} Specially formatted date
 */
function processDate(option) {
  const [quarter, year] = chartHooks.cci_dateToQuarter(option);
  return `${quarter} ${year}`;
}

/**
 * @param {Array} options - List of options to build for the select component
 * @param {object} chartNode - The DOM node of the current chart
 * @param {object} filter - key and possible label to filter on
 * @returns {object} the built select DOM node
 */
function makeSelectFilterDOM(options, chartNode, filter) {
  const id = Math.random() + filter.key;
  const attachPoint = chartNode.getElementsByClassName(
    'o-simple-chart__filters',
  )[0];

  const wrapper = document.createElement('div');
  wrapper.className = 'filter-wrapper m-form-field';

  const label = document.createElement('label');
  label.className = 'a-label a-label--heading';
  label.innerText = filter.label ? filter.label : 'Select ' + filter.key;
  label.htmlFor = id;

  const selectDiv = document.createElement('div');
  selectDiv.className = 'a-select';

  const select = document.createElement('select');
  select.id = id;

  /* Explicitly pass "all" key as part of filter */
  if (filter.all) {
    const allOpt = document.createElement('option');
    allOpt.value = 'View all';
    allOpt.innerText = 'View all';
    select.appendChild(allOpt);
  }

  options.forEach((option) => {
    const opt = document.createElement('option');
    opt.value = option;

    if (filter.key === 'tilemap') opt.innerText = processDate(option);
    else opt.innerText = option;

    select.appendChild(opt);
  });

  selectDiv.appendChild(select);
  wrapper.appendChild(label);
  wrapper.appendChild(selectDiv);
  attachPoint.appendChild(wrapper);

  const selector = {
    nodes: [select],
    filterProp: filter.key,
    value: select.value,
    attach(filterFn) {
      select.addEventListener('change', () => {
        selector.value = select.value;
        filterFn();
      });
      filterFn();
    },
  };

  return selector;
}

/**
 * @param {Array} buckets - List of buckets to build radio inputs from
 * @param {object} chartNode - The DOM node of the current chart
 * @param {object} filter - key and possible label to filter on
 * @returns {object} the built select DOM node
 */
function makeRadioFilterDOM(buckets, chartNode, filter) {
  const attachPoint = chartNode.getElementsByClassName(
    'o-simple-chart__filters',
  )[0];
  const radios = [];

  const wrapper = document.createElement('div');
  wrapper.className = 'filter-wrapper';

  const bucketLabel = document.createElement('h4');
  bucketLabel.innerText = filter.label ? filter.label : 'Select ' + filter.key;

  wrapper.appendChild(bucketLabel);

  /**
   * @param {string} bucket - The bucket on which to filter data
   * @param {number} i - Calling order
   */
  function makeRadioGroup(bucket, i) {
    const id = Math.random() + bucket;
    const radioWrapper = document.createElement('div');
    radioWrapper.className = 'm-form-field m-form-field--radio u-mb5';
    let radioGroupName = document.querySelectorAll('.filter-wrapper').length;
    radioGroupName = 'radio-group_' + radioGroupName;

    const input = document.createElement('input');
    input.className = 'a-radio';
    input.type = 'radio';
    input.id = id;
    input.value = bucket;
    input.name = radioGroupName;
    if (i === 0) input.checked = true;

    const label = document.createElement('label');
    label.className = 'a-label';
    label.htmlFor = id;
    label.innerText = bucket;

    radioWrapper.appendChild(input);
    radioWrapper.appendChild(label);
    wrapper.appendChild(radioWrapper);

    radios.push(input);
  }

  /* Explicitly pass "all" key as part of filter */
  if (filter.all) {
    buckets.unshift('View all');
  }

  buckets.forEach(makeRadioGroup);

  attachPoint.appendChild(wrapper);

  const selector = {
    nodes: radios,
    filterProp: filter.key,
    value: radios[0].value,
    attach(filterFn) {
      radios.forEach((r) => {
        r.addEventListener('change', () => {
          selector.value = r.value;
          filterFn();
        });
      });
      filterFn();
    },
  };

  return selector;
}

/**
 * Filters raw or transformed data by a select prop.
 * @param {Array} data - Transformed or raw chart data.
 * @param {object} filterProp - Key on which to filter.
 * @param {object} filterVal - Value of the selectNode against
 *   which we're filtering.
 * @returns {Array} Filtered chart data.
 */
function filterData(data, filterProp, filterVal) {
  if (filterVal === 'View all') return data;

  return data.filter((d) => {
    const match = d[filterProp];
    if (Array.isArray(match)) return match.indexOf(filterVal) >= 0;
    return match === filterVal;
  });
}

/**
 * Wires up filter elements when provided filters
 * @param {object} dataAttributes - Data passed via data-* tags
 * @param {object} chartNode - The DOM node of the current chart
 * @param {object} chart - The initialized chart
 * @param {object} data - The chart data object, {raw, series, transformed}
 */
function initFilters(dataAttributes, chartNode, chart, data) {
  let filters = dataAttributes.filters;
  if (!filters) return;
  // Allow plain Wagtail strings
  if (!filters.match('{') && !filters.match('"')) {
    filters = `"${filters}"`;
  }

  const rawOrTransformed = data.transformed || data.raw;

  try {
    filters = JSON.parse(filters);
    if (!Array.isArray(filters)) filters = [filters];

    const selectors = [];

    filters.forEach((filter) => {
      const buckets = getDataBuckets(filter, rawOrTransformed);
      if (buckets.length < 6) {
        selectors.push(makeRadioFilterDOM(buckets, chartNode, filter));
      } else {
        selectors.push(makeSelectFilterDOM(buckets, chartNode, filter));
      }
    });

    if (selectors.length) {
      attachFilters(selectors, chart, dataAttributes, rawOrTransformed);
    }
  } catch (err) {
    /* eslint-disable-next-line no-console */
    console.error(err, 'Bad JSON in chart filters ', filters);
  }
}

/**
 * @param {object} selectors - List of selectors that need to be run
 * @param {object} chart - The Highcharts chart object
 * @param {object} dataAttributes - Data passed via data-* tags
 * @param {object} data - Chart data, either raw or transformed
 */
function attachFilters(selectors, chart, dataAttributes, data) {
  const { styleOverrides } = dataAttributes;

  /**
   * Filter data and update the chart on select
   */
  function filterOnSelect() {
    // filter on all selects
    let filtered = data;

    for (let i = 0; i < selectors.length; i++) {
      const selector = selectors[i];
      const { filterProp, value } = selector;
      filtered = filterData(filtered, filterProp, value);
    }

    const filteredSeries = extractSeries(filtered, dataAttributes);
    filteredSeries.forEach((dataSeries) => {
      chart.series.forEach((chartSeries) => {
        if (dataSeries.name === chartSeries.name) {
          chartSeries.setData(dataSeries.data, false);
        }
      });
    });

    const obj = {};

    if (styleOverrides && styleOverrides.match('hook__')) {
      overrideStyles(styleOverrides, obj, filtered);
    }

    chart.update(obj);
  }

  selectors.forEach((selector) => {
    selector.attach(filterOnSelect);
  });
}

export { initFilters };
