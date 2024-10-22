import $ from '../../../../../js/modules/util/dollar-sign.js';
import getFinancial from '../dispatchers/get-financial-values.js';
import getSchool from '../dispatchers/get-school-values.js';
import { formatUSD } from '../../../../../js/modules/util/format.js';

const metricView = {
  metrics: {
    debtBurden: {
      school: NaN,
      national: 0.08,
      low: 0.075,
      high: 0.085,
      better: 'lower',
      standing: '',
    },
    gradRate: {
      school: NaN,
      national: NaN,
      nationalKey: 'completionRateMedian',
      better: 'higher',
      format: 'decimal-percent',
      standing: '',
      source: 'unknown',
    },
    defaultRate: {
      school: NaN,
      national: NaN,
      nationalKey: 'loanDefaultRate',
      better: 'lower',
      format: 'decimal-percent',
      standing: '',
      source: 'unknown',
    },
  },

  // Flag if this is a settlement school.
  settlementStatus: false,

  /**
   * Initiates the object
   */
  init: function () {
    this.settlementStatus = getSchool.values().settlementSchool || false;
    this.setMetrics(this.metrics);
    this.updateDebtBurden();
  },

  /**
   * Helper function which sets up metrics data
   * @param {object} metrics - An object of metrics
   * @returns {object} metrics with additional values added
   */
  setMetrics: function (metrics) {
    const graphKeys = ['gradRate', 'defaultRate'];
    const financials = getFinancial.values();
    for (let x = 0; x < graphKeys.length; x++) {
      const key = graphKeys[x];
      const nationalKey = metricView.metrics[key].nationalKey;

      metrics[key].school = financials[key];
      metrics[key].national = financials[nationalKey];
      metrics[key].low = financials[nationalKey + 'Low'];
      metrics[key].high = financials[nationalKey + 'High'];
      metrics[key].source = financials[key + 'Source'];
      metrics[key] = metricView.checkMetrics(metrics[key]);
    }
    return metrics;
  },

  /**
   * Helper function that checks metric object to determine if they
   * are better or worse than the national metric
   * @param {object} metrics - the metrics object
   * @returns {string} the result of the check
   */
  checkMetrics: function (metrics) {
    let sign = 1;

    if (metrics.better === 'lower') {
      sign = -1;
    }
    const high = metrics.high * sign;
    const low = metrics.low * sign;
    const school = Number(metrics.school) * sign;
    if (high < school) {
      metrics.standing = 'better';
    } else if (low > school) {
      metrics.standing = 'worse';
    } else {
      metrics.standing = 'same';
    }
    return metrics;
  },

  /**
   * Helper function that updates the value or text of an element
   * @param {object} $ele - jQuery object of the element to update
   * @param {number|string} value - The new value
   * @param {boolean} format - Type of number, for formatting
   */
  updateText: function ($ele, value, format) {
    if (format === 'currency') {
      value = formatUSD({ amount: value, decimalPlaces: 0 });
    }
    if (format === 'decimal-percent') {
      value = Math.round(value * 100).toString() + '%';
    }
    $ele.text(value);
  },

  /**
   * Fixes overlapping points on a bar graph
   * @param {object} $graph - jQuery object of the graph containing the points
   */
  fixOverlap: function ($graph) {
    const $school = $graph.find('[data-bar-graph_number="you"]');
    const $national = $graph.find('[data-bar-graph_number="average"]');
    const metricKey = $graph.attr('data-metric');
    const metrics = metricView.metrics[metricKey];
    const schoolHeight = $school.find('.bar-graph__label').height();
    const schoolTop = $school.top();
    const nationalHeight = $national.find('.bar-graph__label').height();
    const nationalTop = $national.top();
    let $higherPoint = $national;
    let $lowerPoint = $school;
    // nationalPointHeight is the smaller and gives just the right offset
    const offset = nationalHeight - Math.abs(schoolTop - nationalTop);

    // Check $higherPoint
    if (schoolTop > nationalTop) {
      $higherPoint = $school;
      $lowerPoint = $national;
    }
    const $higherLabels = $higherPoint.find(
      '.bar-graph__label, .bar-graph__value',
    );

    // If the values are equal, handle the display with CSS only
    if (metrics.school === metrics.national) {
      $graph.addClass('bar-graph--equal');
      return;
    }
    // If the points partially overlap, move the higher point's labels up
    if (
      nationalTop <= schoolTop + schoolHeight &&
      nationalTop + nationalHeight >= schoolTop
    ) {
      $higherLabels.each((elem) => {
        elem.style.paddingBottom = offset;
        elem.style.top = -offset;
      });

      /* Need to reset the z-index since fixOverlap is called on page load and
         again when a verification button is clicked */
      $higherPoint.each((elem) => {
        elem.style.zIndex = 'auto';
      });
      $lowerPoint.each((elem) => {
        elem.style.zIndex = 100;
      });
    }
  },

  /**
   * Sets text of each point on a bar graph (or a class if a point is missing)
   * @param {object} $graph - jQuery object of the graph containing the points
   */
  setGraphValues: function ($graph) {
    const $school = $graph.find('[data-bar-graph_number="you"]');
    const $national = $graph.find('[data-bar-graph_number="average"]');
    const metricKey = $graph.attr('data-metric');
    const metrics = metricView.metrics[metricKey];
    if (isNaN(metrics.school)) {
      $graph.addClass('bar-graph--missing-you');
    } else {
      this.updateText($school, metrics.school, metrics.format);
    }
    if (isNaN(metrics.national)) {
      $graph.addClass('bar-graph--missing-average');
    } else {
      this.updateText($national, metrics.national, metrics.format);
    }
  },

  /**
   * Sets the position of each point on a bar graph
   * @param {object} $graph - jQuery object of the graph containing the points
   */
  setGraphPositions: function ($graph) {
    // schoolValue, nationalValue, $school, $national
    const graphHeight = $graph.height();
    const metricKey = $graph.attr('data-metric');
    const nationalValue = metricView.metrics[metricKey].national;
    const schoolValue = metricView.metrics[metricKey].school;
    const min = $graph.attr('data-graph-min');
    const max = $graph.attr('data-graph-max');
    const $school = $graph.find('.bar-graph__point--you');
    const $national = $graph.find('.bar-graph__point--average');
    const bottoms = {};
    const bottomOffset = 20;

    bottoms.school =
      ((graphHeight - bottomOffset) / (max - min)) * (schoolValue - min) +
      bottomOffset;
    bottoms.national =
      ((graphHeight - bottomOffset) / (max - min)) * (nationalValue - min) +
      bottomOffset;

    /* A few outlier schools have very high average salaries, so we need to
       prevent those values from falling off the top of the graph */
    if (schoolValue > max) {
      bottoms.school = graphHeight;
      $graph.addClass('bar-graph--high-point');
    }
    $school.each((elem) => {
      elem.style.bottom = bottoms.school + 'px';
    });
    $national.each((elem) => {
      elem.style.bottom = bottoms.national + 'px';
    });
  },

  /**
   * Classifies school value in relation to the national average
   * @param {number|NaN} metricKey - metric to be checked
   * @returns {string} Classes to add to the notification box
   */
  getNotifications: function (metricKey) {
    let classes = 'cf-notification ';
    const standingClasses = {
      same: 'metric__notification--same',
      better: 'metric__notification--better',
      worse:
        'cf-notification metric__notification--worse ' +
        'cf-notification--error',
    };
    const metrics = metricView.metrics[metricKey];
    const low = metrics.low;
    const high = metrics.high;

    /* Check if there are warnings, if the school metric is about the
       same, better, or worse than the national metric, and if there
       is an error. */
    const warnings = this.checkWarnings(metrics.school, metrics.national);
    classes = standingClasses[metrics.standing];

    if (isNaN(low) || isNaN(high)) {
      classes = '';
    }
    // if either warnings (if not false) or classes
    return warnings || classes;
  },

  /**
   * @param {number} schoolValue - metric value of school
   * @param {number} nationalValue - metric national average
   * @returns {string} Warning classes based on values
   */
  checkWarnings: function (schoolValue, nationalValue) {
    let classes = 'cf-notification ';
    if (isNaN(schoolValue) && isNaN(nationalValue)) {
      classes += 'metric__notification--no-data cf-notification--warning';
      return classes;
    } else if (isNaN(schoolValue)) {
      classes += 'metric__notification--no-you cf-notification--warning';
      return classes;
    } else if (isNaN(nationalValue)) {
      classes += 'metric__notification--no-average cf-notification--warning';
      return classes;
    }

    return false;
  },

  /**
   * Adds the correct classes to metric notification boxes.
   * @param {object} $notification - jQuery object of the notification box.
   * @param {string} notificationClasses - Classes to add to the notification.
   */
  setNotificationClasses: function ($notification, notificationClasses) {
    $notification.attr('class', 'metric__notification');
    $notification.addClass(notificationClasses);
  },

  /**
   * Hides the metric notification boxes for settlement schools.
   * @param {object} $notification - jQuery object of the notification box.
   */
  hideNotificationClasses: function ($notification) {
    $notification.attr('class', 'metric__notification');
    $notification.hide();
  },

  /**
   * Initializes all metrics with bar graphs.
   */
  updateGraphs: function () {
    const $graphs = $('.bar-graph');
    $graphs.each((elem) => {
      const $graph = $(elem);
      const metricKey = $graph.attr('data-metric');
      const notificationClasses = metricView.getNotifications(metricKey);
      const $notification = $graph.siblings('.metric__notification');

      metricView.setGraphValues($graph);
      metricView.setGraphSources($graph);
      metricView.setGraphPositions($graph);
      metricView.fixOverlap($graph);
      metricView.setNotificationClasses($notification, notificationClasses);
      if (metricView.settlementStatus === true) {
        metricView.updateForSettlement($graph);
      }
    });
  },

  /**
   * Calculates the student's debt burden.
   * @param {number} monthlyLoanPayment - Student's monthly loan payment after
   *   graduation.
   * @param {monthlySalary} monthlySalary - Student's estimated monthly salary
   *   after graduation.
   * @returns {number} Student's debt burden.
   */
  calculateDebtBurden: function (monthlyLoanPayment, monthlySalary) {
    const debtBurden = monthlyLoanPayment / monthlySalary;
    return debtBurden;
  },

  /**
   * Calculates a monthly salary from an annual salary.
   * @param {number} annualSalary - Annual salary.
   * @returns {number} Monthly salary.
   */
  calculateMonthlySalary: function (annualSalary) {
    const monthlySalary = annualSalary / 12;
    return monthlySalary;
  },

  /**
   * Populates the debt burden numbers and shows the corresponding notification
   * on the page.
   */
  updateDebtBurden: function () {
    const $section = $('[data-repayment-section="debt-burden"]');
    const $elements = $section.find('[data-debt-burden]');
    const financials = getFinancial.values();
    const values = {};
    const $notification = $('.debt-burden .metric__notification');

    // Calculate values
    values.loanMonthly = financials.loanMonthly;
    values.annualSalary = financials.medianSalary;
    values.monthlySalary = values.annualSalary / 12;
    values.debtBurden = values.loanMonthly / values.monthlySalary;

    // Update debt burden elements
    $elements.each((elem) => {
      const $ele = $(elem);
      const prop = $ele.attr('data-debt-burden');
      let format = 'currency';
      if (prop === 'debtBurden') {
        format = 'decimal-percent';
      }
      metricView.updateText($ele, values[prop], format);
    });

    const selecter = this.getNotifications('debtBurden');

    if (this.settlementStatus === false) {
      this.setNotificationClasses($notification, selecter);
    } else {
      this.hideNotificationClasses($notification);
    }
  },

  /**
   * Updates salary metric with warning about no program or school data for
   * settlement schools.
   */
  updateSalaryWarning: function () {
    const $salaryDebt = $('#salary-and-debt-metric');
    const notificationClasses =
      'cf-notification metric__notification--no-you cf-notification--warning';
    const $notification = $salaryDebt.siblings('.metric__notification');

    metricView.setNotificationClasses($notification, notificationClasses);
  },

  /**
   * Updates graph content with source - Program or School.
   * @param {object} $graph - jQuery object of the graph containing the points.
   */
  setGraphSources: function ($graph) {
    const metricKey = $graph.attr('data-metric');
    const source = metricView.metrics[metricKey].source;
    const text = 'This ' + source;
    const $ele = $graph.find('[data-graph_label]');

    $ele.text(text);
    if (metricKey === 'gradRate' && source === 'school') {
      $('.content-grad-program').hide();
    }
    if (metricKey === 'defaultRate' && source === 'school') {
      $('.content-default-program').text(source);
    }
  },

  /**
   * Updates view for settlement schools.
   * @param {object} $graph - jQuery object of the graph.
   */
  updateForSettlement: function ($graph) {
    const $notification = $graph.siblings('.metric__notification');
    const selector =
      '.metric__notification--no-you,.metric__notification--no-data';
    $notification.not(selector).hide();
    $graph.find('.bar-graph__point--average').hide();
  },
};

export default metricView;
