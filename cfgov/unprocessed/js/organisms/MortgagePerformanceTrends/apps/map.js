import * as ccb from '../../../../apps/cfpb-chart-builder/js';
import MapStore from '../stores/map';
import actions from '../actions/map';
import utils from '../utils';

const _plurals = {
  state: 'states',
  metro: 'metros',
  county: 'counties',
};

class MortgagePerformanceMap {
  constructor({ container }) {
    this.$container = document.getElementById(container);
    this.$form = this.$container.querySelector('#mp-map-controls');
    this.$geo = this.$container.querySelector('#mp-map-geo');
    this.$state = this.$container.querySelector('#mp-map-state');
    this.$metro = this.$container.querySelector('#mp-map-metro');
    this.$county = this.$container.querySelector('#mp-map-county');
    this.$month = this.$container.querySelector('#mp-map-month');
    this.$year = this.$container.querySelector('#mp-map-year');
    this.$map = this.$container.querySelector('#mp-map');
    this.$mapTitle = document.querySelector('#mp-map-title-status');
    this.$mapTitleLocation = document.querySelector('#mp-map-title-location');
    this.$mapTitleDate = document.querySelector('#mp-map-title-date');
    this.$notification = document.querySelector('#mp-map-notification');
    this.timespan = this.$container.getAttribute('data-chart-time-span');
    this.startDate = this.$container.getAttribute('data-chart-start-date');
    this.endDate = this.$container.getAttribute('data-chart-end-date');
    this.endMonth = utils.getMonth(this.endDate);
    this.endYear = utils.getYear(this.endDate);
    const date = `${this.endYear}-${this.endMonth}`;
    this.store = new MapStore({
      date,
      middleware: [utils.thunkMiddleware, utils.loggerMiddleware],
    });
    this.$chart = this.$container.querySelector('#mp-map');
    this.chart = ccb.createChart({
      el: this.$chart,
      source: `map-data/${this.timespan}/states/${date}`,
      type: 'geo-map',
      color: this.$container.getAttribute('data-chart-color'),
      metadata: 'states',
      tooltipFormatter: this.renderTooltip(),
    });
    this.$chart.setAttribute('data-chart-ignore', 'true');
    this.eventListeners();
    this.renderYears();
    this.setDate();
  }
}

MortgagePerformanceMap.prototype.eventListeners = function () {
  this.$form.addEventListener('change', this.onChange.bind(this));
  this.store.subscribe(this.renderChart.bind(this));
  this.store.subscribe(this.renderChartTitle.bind(this));
  this.store.subscribe(this.renderChartForm.bind(this));
  this.store.subscribe(this.renderCounties.bind(this));
  this.store.subscribe(this.renderMetros.bind(this));
};

MortgagePerformanceMap.prototype.onClick = function (event) {
  const change = new Event('change');
  this.$container.querySelector('input[name="mp-map_geo"]:checked').checked =
    false;
  this.$form.dispatchEvent(change);
  event.preventDefault();
};

MortgagePerformanceMap.prototype.onChange = function (event) {
  let action;
  let geoId;
  let geoName;
  let date;

  const abbr =
    this.$state.options[this.$state.selectedIndex].getAttribute('data-abbr');
  const geoType = this.$container
    .querySelector('input[name="mp-map_geo"]:checked')
    .id.replace('mp-map_geo-', '');

  switch (event.target.id) {
    case 'mp-map_geo-state':
    case 'mp-map_geo-metro':
    case 'mp-map_geo-county':
      geoId = '';
      geoName = '';
      action = actions.updateChart(geoId, geoName, geoType);
      // If a state has been pre-selected, populate the metros dropdown
      if (abbr && geoType === 'metro') {
        this.store.dispatch(actions.fetchMetros(abbr));
      }
      // If a state has been pre-selected, populate the counties dropdown
      if (abbr && geoType === 'county') {
        this.store.dispatch(actions.fetchCounties(abbr));
      }
      break;
    case 'mp-map-state':
      // If no state is selected, zoom out and abort
      if (!abbr) {
        this.chart.highchart.chart.mapZoom();
        utils.setZoomLevel(10);
        action = actions.updateChart('', '', geoType);
        break;
      }
      if (geoType === 'metro') {
        action = actions.fetchMetros(abbr, true);
        break;
      }
      if (geoType === 'county') {
        action = actions.fetchCounties(abbr, true);
        break;
      }
      geoId = this.$state.value;
      geoName = this.$state.options[this.$state.selectedIndex].text;
      action = actions.updateChart(geoId, geoName, geoType);
      break;
    case 'mp-map-metro':
      geoId = this.$metro.value;
      if (!geoId) {
        action = actions.zoomChart(abbr);
        break;
      }
      geoName = this.$metro.options[this.$metro.selectedIndex].text;
      action = actions.updateChart(geoId, geoName);
      break;
    case 'mp-map-county':
      geoId = this.$county.value;
      if (!geoId) {
        action = actions.zoomChart(abbr);
        break;
      }
      geoName = this.$county.options[this.$county.selectedIndex].text;
      action = actions.updateChart(geoId, geoName);
      break;
    case 'mp-map-month':
    case 'mp-map-year':
      date = `${this.$year.value}-${this.$month.value}`;
      action = actions.updateDate(date);
      break;
    default:
      action = actions.clearGeo();
  }

  return this.store.dispatch(action);
};

MortgagePerformanceMap.prototype.renderChart = function (prevState, state) {
  const prevType = prevState.geo.type;
  const currType = state.geo.type;
  const prevId = prevState.geo.id;
  const currId = state.geo.id;
  let zoomLevel;
  if (!utils.isDateValid(state.date, this.endDate)) {
    this.$notification.classList.add('m-notification--visible');
    return;
  }
  this.$notification.classList.remove('m-notification--visible');
  if (prevId && prevId !== currId) {
    this.chart.highchart.chart.get(prevId).select(false);
  }
  if (prevState.date === state.date && prevType === currType && currId) {
    /* Highcharts zooming is unreliable and difficult to customize :(
       https://api.highcharts.com/class-reference/Highcharts.Chart.html#mapZoom
       If it's a state or non-metro, zoom in more than other location types */
    zoomLevel = currType === 'state' || utils.isNonMetro(currId) ? 5 : 10;
    this.chart.highchart.chart.get(currId).select(true);
    this.chart.highchart.chart.get(currId).zoomTo();
    this.chart.highchart.chart.mapZoom(zoomLevel);
  }
  if (state.zoomTarget) {
    const centroid = utils.stateCentroids[state.zoomTarget];
    this.chart.highchart.chart.mapZoom();
    utils.setZoomLevel(10);
    zoomLevel = utils.getZoomLevel(5);
    this.chart.highchart.chart.mapZoom(zoomLevel, centroid[0], centroid[1]);
  }
  // If no geo is selected, ensure metro and county dropdowns are cleared
  if (!currId || prevType !== currType) {
    this.$metro.value = '';
    this.$metro.innerHTML = '';
    this.$county.value = '';
    this.$county.innerHTML = '';
  }
  if (prevState.date !== state.date || prevType !== currType) {
    // this.store.dispatch( actions.startLoading() );
    this.chart.highchart.chart.showLoading();
    this.chart
      .update({
        source: `map-data/${this.timespan}/${_plurals[currType]}/${state.date}`,
        metadata: _plurals[currType],
        tooltipFormatter: this.renderTooltip(),
      })
      .then(() => {
        // this.store.dispatch( actions.stopLoading() );
        if (prevState.date !== state.date && currId) {
          this.chart.highchart.chart.get(currId).select(true);
        }
      });
  }
};

MortgagePerformanceMap.prototype.renderChartForm = function (prevState, state) {
  let geoType = state.geo.type;
  if (state.isLoadingCounties) {
    geoType = 'county';
  }
  if (state.isLoadingMetros) {
    geoType = 'metro';
  }
  const geo = this.$container.querySelector(`#mp-map-${geoType}-container`);
  const containers = this.$container.querySelectorAll(
    '.mp-map-select-container',
  );
  for (let i = 0; i < containers.length; ++i) {
    utils.hideEl(containers[i]);
  }
  if (geoType === 'county' || geoType === 'metro') {
    utils.showEl(this.$container.querySelector('#mp-map-state-container'));
  }
  if (geo) {
    utils.showEl(geo);
  }
  return geoType;
};

MortgagePerformanceMap.prototype.renderChartTitle = function (
  prevState,
  state,
) {
  let loc = state.geo.name;
  if (!utils.isDateValid(state.date, this.endDate)) {
    return;
  }
  if (!loc) {
    loc = `${state.geo.type} view`;
  } else if (state.geo.type === 'county') {
    loc = `${loc}, ${utils.getCountyState(state.geo.id)}`;
  }
  this.$mapTitleLocation.innerText = loc;
  this.$mapTitleDate.innerText = utils.getDate(state.date);
};

MortgagePerformanceMap.prototype.renderCounties = function (prevState, state) {
  let option;
  this.$county.disabled = state.isLoadingCounties;
  // If there are no counties to render, abort.
  if (!state.counties || !state.counties.length) {
    this.$county.disabled = true;
    return;
  }
  // If a county is actively selected and they haven't changed, abort.
  if (this.$county.value && !prevState.isLoadingCounties) {
    return;
  }
  state.counties.sort((a, b) => (a.name < b.name ? -1 : 1));
  const fragment = document.createDocumentFragment();
  option = utils.addOption({
    document,
    value: '',
    text: 'Please select a county',
  });
  fragment.appendChild(option);
  state.counties.forEach((county) => {
    option = utils.addOption({
      document,
      value: county.fips,
      text: county.name,
    });
    fragment.appendChild(option);
  });
  this.$county.innerHTML = '';
  this.$county.appendChild(fragment);
};

MortgagePerformanceMap.prototype.renderMetros = function (prevState, state) {
  let option, nonMSA;
  this.$metro.disabled = state.isLoadingMetros;
  // If there are no metros to render, abort.
  if (!state.metros || !state.metros.length) {
    this.$metro.disabled = true;
    return;
  }
  // If a metro is actively selected and they haven't changed, abort.
  if (this.$metro.value && !prevState.isLoadingMetros) {
    return;
  }
  // Alphabetize mero names
  state.metros.sort((a, b) => (a.name < b.name ? -1 : 1));
  // Pull out any non-metros and put them at the end.
  state.metros = state.metros.filter((metro) => {
    if (utils.isNonMetro(metro.fips)) {
      nonMSA = {
        fips: metro.fips,
        name: metro.name,
      };
      return false;
    }
    return true;
  });
  if (nonMSA) {
    state.metros.push(nonMSA);
  }
  const fragment = document.createDocumentFragment();
  option = utils.addOption({
    document,
    value: '',
    text: 'Please select an area',
  });
  fragment.appendChild(option);
  state.metros.forEach((metro) => {
    option = utils.addOption({
      document,
      value: metro.fips,
      text: metro.name,
    });
    fragment.appendChild(option);
  });
  this.$metro.innerHTML = '';
  this.$metro.appendChild(fragment);
};

MortgagePerformanceMap.prototype.setDate = function () {
  const month = this.$month.querySelector(`option[value="${this.endMonth}"]`);
  const year = this.$year.querySelector(`option[value="${this.endYear}"]`);
  month.setAttribute('selected', 'selected');
  year.setAttribute('selected', 'selected');
};

MortgagePerformanceMap.prototype.renderYears = function () {
  const fragment = document.createDocumentFragment();
  let startYear = utils.getYear(this.startDate);
  const endYear = utils.getYear(this.endDate);
  let option = utils.addOption({
    document,
    value: startYear,
    text: startYear,
  });
  fragment.appendChild(option);
  while (startYear++ < endYear) {
    option = utils.addOption({
      document,
      value: startYear,
      text: startYear,
    });
    fragment.appendChild(option);
  }
  this.$year.innerHTML = '';
  this.$year.appendChild(fragment);
};

MortgagePerformanceMap.prototype.renderTooltip = function () {
  return (point, meta) => {
    let percent;
    const nationalPercent = Math.round(meta.national_average * 1000) / 10;
    if (point.value === null) {
      return "<div class='m-mp-map-tooltip'>Insufficient data for this area</div>";
    }
    if (point.value < 0) {
      percent = 'Insufficient data';
    } else {
      percent = Math.round(point.value * 10) / 10;
      percent = `<strong>${percent}%</strong> mortgage delinquency rate`;
    }
    return `<dl class='m-mp-map-tooltip'>
      <dt>${point.name}</dt>
      <dd>${percent}</dd>
      <dd><strong>${nationalPercent}%</strong> national average</dd>
    </dl>`;
  };
};

export default MortgagePerformanceMap;
