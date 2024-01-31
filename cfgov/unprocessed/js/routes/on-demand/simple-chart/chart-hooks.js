/* eslint camelcase: [0] */
const cci_quarterRange = {
  'Mar 31': 'Jan-Mar',
  'Jun 30': 'Apr-Jun',
  'Sep 30': 'Jul-Sep',
  'Dec 31': 'Oct-Dec',
};

const cci_quarterMap = {
  'Mar 31': 'Q1',
  'Jun 30': 'Q2',
  'Sep 30': 'Q3',
  'Dec 31': 'Q4',
};

const msYear = 365 * 24 * 60 * 60 * 1000;

/**
 *
 * @param {string} age - Age to pluck from the data
 * @returns {Function} A hook function
 */
function make_cct_age_yoy(age) {
  return (d) =>
    d[age].map((v) => {
      return {
        x: v[0],
        percent: v[1] * 100,
      };
    });
}

const hooks = {
  // Example transform
  monotonicY(data) {
    return data.map((item, i) => ({
      ...item,
      y: i + 1,
    }));
  },

  cct_yoy_transform(d) {
    return d['Number of Loans'].map((v, i) => {
      return {
        x: v[0],
        loans: v[1] * 100,
        volume: d['Dollar Volume'][i][1] * 100,
      };
    });
  },

  cct_age_yoy_30(d) {
    return make_cct_age_yoy('Younger than 30')(d);
  },

  cct_age_yoy_30_44(d) {
    return make_cct_age_yoy('30-44')(d);
  },

  cct_age_yoy_45_64(d) {
    return make_cct_age_yoy('45-64')(d);
  },

  cct_age_yoy_65(d) {
    return make_cct_age_yoy('65 and older')(d);
  },

  cct_age_30(d) {
    return d.filter((v) => v.age_group === 'Younger than 30');
  },

  cct_age_30_44(d) {
    return d.filter((v) => v.age_group === 'Age 30-44');
  },

  cct_age_45_64(d) {
    return d.filter((v) => v.age_group === 'Age 45-64');
  },

  cct_age_65(d) {
    return d.filter((v) => v.age_group === 'Age 65 and older');
  },

  getDateString(x) {
    return new Date(x).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      timeZone: 'UTC',
    });
  },

  cci_quarterLabels() {
    const { x, y, series } = this;
    const titleObj = series.yAxis.axisTitle;
    const title = titleObj ? titleObj.textStr + ': ' : '';
    const [quarter, year] = hooks.cci_dateToQuarter(x);
    return `<b>${series.name}</b><br/>${quarter} ${year}<br/>${title}${
      Math.round(y * 10) / 10
    }`;
  },

  cci_dateToQuarter(x) {
    const d = hooks.getDateString(x).split(', ');
    const quarter = `${cci_quarterMap[d[0]]}: ${cci_quarterRange[d[0]]}`;
    const year = d[1];
    return [quarter, year];
  },

  cci_tickPositioner() {
    const { series, min, max } = this;
    if ((max - min) / msYear > 5) return this.tickPositions;
    let ticks = series[0].xData.filter((v) => v >= min && v <= max);
    if (ticks.length > 9) {
      ticks = ticks.filter((v, i) => i % 2 === 0);
    }
    return ticks;
  },

  cci_xAxisLabels() {
    const { min, max } = this.chart.xAxis[0];
    const d = new Date(this.value);
    if ((max - min) / msYear > 5) {
      return d.getFullYear() + 1;
    }

    const dSplit = hooks.getDateString(d).split(', ');
    return `${cci_quarterMap[dSplit[0]]}<br/>${dSplit[1]}`;
  },

  enforcement_yAxisLabelsFormatter() {
    return `$${Math.round(this.value / 1e9)}B`;
  },

  enforcement_barTooltipFormatter() {
    return `<b>${this.x}</b><br/>Total enforcement actions: <b>${this.y}</b>`;
  },

  enforcement_reliefBarTooltipFormatter() {
    return `<b>${
      this.x
    }</b><br/>Total relief: <b>$${this.y.toLocaleString()}</b>`;
  },

  cct_credit(data) {
    const raw = {};
    const adjusted = {};
    data.forEach((v) => {
      let currRaw, currAdj;
      if (raw[v.date]) {
        currRaw = raw[v.date];
        currAdj = adjusted[v.date];
      } else {
        currRaw = raw[v.date] = { date: v.date, adjusted: 'Unadjusted' };
        currAdj = adjusted[v.date] = {
          date: v.date,
          adjusted: 'Seasonally adjusted',
        };
      }
      currRaw[v.credit_score_group] = v.vol_unadj;
      currAdj[v.credit_score_group] = v.vol;
    });

    const newData = [];
    [adjusted, raw].forEach((obj) => {
      for (const [, v] of Object.entries(obj)) {
        newData.push(v);
      }
    });

    return newData.sort((a, b) => new Date(a.date) - new Date(b.date));
  },

  /* TODO: Create a hook that accounts for both
     credit_score_group and income_level_group */
  cct_income(data) {
    const raw = {};
    const adjusted = {};
    data.forEach((v) => {
      let currRaw, currAdj;
      if (raw[v.date]) {
        currRaw = raw[v.date];
        currAdj = adjusted[v.date];
      } else {
        currRaw = raw[v.date] = { date: v.date, adjusted: 'Unadjusted' };
        currAdj = adjusted[v.date] = {
          date: v.date,
          adjusted: 'Seasonally adjusted',
        };
      }
      currRaw[v.income_level_group] = v.vol_unadj;
      currAdj[v.income_level_group] = v.vol;
    });

    const newData = [];
    [adjusted, raw].forEach((obj) => {
      for (const [, v] of Object.entries(obj)) {
        newData.push(v);
      }
    });

    return newData.sort((a, b) => new Date(a.date) - new Date(b.date));
  },

  cct_age(data) {
    const raw = {};
    const adjusted = {};
    data.forEach((v) => {
      let currRaw, currAdj;
      if (raw[v.date]) {
        currRaw = raw[v.date];
        currAdj = adjusted[v.date];
      } else {
        currRaw = raw[v.date] = { date: v.date, adjusted: 'Unadjusted' };
        currAdj = adjusted[v.date] = {
          date: v.date,
          adjusted: 'Seasonally adjusted',
        };
      }
      currRaw[v.age_group] = v.vol_unadj;
      currAdj[v.age_group] = v.vol;
    });

    const newData = [];
    [adjusted, raw].forEach((obj) => {
      for (const [, v] of Object.entries(obj)) {
        newData.push(v);
      }
    });

    return newData.sort((a, b) => new Date(a.date) - new Date(b.date));
  },

  /* Convert YoY fields from decimals to percentages
     e.g. .308798278 becomes 30.88% */
  cct_yoy(data) {
    data = data.map((datum) => {
      for (const [k, v] of Object.entries(datum)) {
        if (k.endsWith('_yoy')) {
          datum[k] = Math.round(v * 10000) / 100;
        }
      }
      return datum;
    });

    return data.sort((a, b) => new Date(a.date) - new Date(b.date));
  },

  /* Convert Credit Tightness Index to allow filterable selection between Unadjusted and Seasonally Adjusted income data sets (MTG/AUTO/CC) */
  cct_crti_income_filterable(data) {
    data = data.reduce((newData, datum) => {
      newData.push({
        high_income:
          datum.nsa_auto_crti_incHigh ||
          datum.nsa_mtg_crti_incHigh ||
          datum.nsa_cc_crti_incHigh,
        moderate_income:
          datum.nsa_auto_crti_incModerate ||
          datum.nsa_mtg_crti_incModerate ||
          datum.nsa_cc_crti_incModerate,
        middle_income:
          datum.nsa_auto_crti_incMiddle ||
          datum.nsa_mtg_crti_incMiddle ||
          datum.nsa_cc_crti_incMiddle,
        low_income:
          datum.nsa_auto_crti_incLow ||
          datum.nsa_mtg_crti_incLow ||
          datum.nsa_cc_crti_incLow,
        date: datum.date,
        adjustment: 'Unadjusted',
      });
      newData.push({
        high_income:
          datum.sa_auto_crti_incHigh ||
          datum.sa_mtg_crti_incHigh ||
          datum.sa_cc_crti_incHigh,
        moderate_income:
          datum.sa_auto_crti_incModerate ||
          datum.sa_mtg_crti_incModerate ||
          datum.sa_cc_crti_incModerate,
        middle_income:
          datum.sa_auto_crti_incMiddle ||
          datum.sa_mtg_crti_incMiddle ||
          datum.sa_cc_crti_incMiddle,
        low_income:
          datum.sa_auto_crti_incLow ||
          datum.sa_mtg_crti_incLow ||
          datum.sa_cc_crti_incLow,
        date: datum.date,
        adjustment: 'Seasonally Adjusted',
      });
      return newData;
    }, []);

    return data.sort((a, b) => new Date(a.date) - new Date(b.date));
  },

  /* Convert Credit Inquiries to allow filterable selection between Unadjusted and Seasonally Adjusted income data sets (MTG/AUTO/CC) */
  cct_inqi_income_filterable(data) {
    data = data.reduce((newData, datum) => {
      newData.push({
        high_income:
          datum.nsa_auto_inqi_incHigh ||
          datum.nsa_mtg_inqi_incHigh ||
          datum.nsa_cc_inqi_incHigh,
        moderate_income:
          datum.nsa_auto_inqi_incModerate ||
          datum.nsa_mtg_inqi_incModerate ||
          datum.nsa_cc_inqi_incModerate,
        middle_income:
          datum.nsa_auto_inqi_incMiddle ||
          datum.nsa_mtg_inqi_incMiddle ||
          datum.nsa_cc_inqi_incMiddle,
        low_income:
          datum.nsa_auto_inqi_incLow ||
          datum.nsa_mtg_inqi_incLow ||
          datum.nsa_cc_inqi_incLow,
        date: datum.date,
        adjustment: 'Unadjusted',
      });
      newData.push({
        high_income:
          datum.sa_auto_inqi_incHigh ||
          datum.sa_mtg_inqi_incHigh ||
          datum.sa_cc_inqi_incHigh,
        moderate_income:
          datum.sa_auto_inqi_incModerate ||
          datum.sa_mtg_inqi_incModerate ||
          datum.sa_cc_inqi_incModerate,
        middle_income:
          datum.sa_auto_inqi_incMiddle ||
          datum.sa_mtg_inqi_incMiddle ||
          datum.sa_cc_inqi_incMiddle,
        low_income:
          datum.sa_auto_inqi_incLow ||
          datum.sa_mtg_inqi_incLow ||
          datum.sa_cc_inqi_incLow,
        date: datum.date,
        adjustment: 'Seasonally Adjusted',
      });
      return newData;
    }, []);

    return data.sort((a, b) => new Date(a.date) - new Date(b.date));
  },

  /* Convert Credit Tightness Index to allow filterable selection between Unadjusted and Seasonally Adjusted age data sets (MTG/AUTO/CC) */
  cct_crti_age_filterable(data) {
    data = data.reduce((newData, datum) => {
      newData.push({
        age_18_29:
          datum.nsa_auto_crti_age18to29 ||
          datum.nsa_mtg_crti_age18to29 ||
          datum.nsa_cc_crti_age18to29,
        age_30_44:
          datum.nsa_auto_crti_age30to44 ||
          datum.nsa_mtg_crti_age30to44 ||
          datum.nsa_cc_crti_age30to44,
        age_45_64:
          datum.nsa_auto_crti_age45to64 ||
          datum.nsa_mtg_crti_age45to64 ||
          datum.nsa_cc_crti_age45to64,
        age_65_plus:
          datum.nsa_auto_crti_age65plus ||
          datum.nsa_mtg_crti_age65plus ||
          datum.nsa_cc_crti_age65plus,
        date: datum.date,
        adjustment: 'Unadjusted',
      });
      newData.push({
        age_18_29:
          datum.sa_auto_crti_age18to29 ||
          datum.sa_mtg_crti_age18to29 ||
          datum.sa_cc_crti_age18to29,
        age_30_44:
          datum.sa_auto_crti_age30to44 ||
          datum.sa_mtg_crti_age30to44 ||
          datum.sa_cc_crti_age30to44,
        age_45_64:
          datum.sa_auto_crti_age45to64 ||
          datum.sa_mtg_crti_age45to64 ||
          datum.sa_cc_crti_age45to64,
        age_65_plus:
          datum.sa_auto_crti_age65plus ||
          datum.sa_mtg_crti_age65plus ||
          datum.sa_cc_crti_age65plus,
        date: datum.date,
        adjustment: 'Seasonally Adjusted',
      });
      return newData;
    }, []);

    return data.sort((a, b) => new Date(a.date) - new Date(b.date));
  },

  /* Convert Credit Inquiries to allow filterable selection between Unadjusted and Seasonally Adjusted age data sets (MTG/AUTO/CC) */
  cct_inqi_age_filterable(data) {
    data = data.reduce((newData, datum) => {
      newData.push({
        age_18_29:
          datum.nsa_auto_inqi_age18to29 ||
          datum.nsa_mtg_inqi_age18to29 ||
          datum.nsa_cc_inqi_age18to29,
        age_30_44:
          datum.nsa_auto_inqi_age30to44 ||
          datum.nsa_mtg_inqi_age30to44 ||
          datum.nsa_cc_inqi_age30to44,
        age_45_64:
          datum.nsa_auto_inqi_age45to64 ||
          datum.nsa_mtg_inqi_age45to64 ||
          datum.nsa_cc_inqi_age45to64,
        age_65_plus:
          datum.nsa_auto_inqi_age65plus ||
          datum.nsa_mtg_inqi_age65plus ||
          datum.nsa_cc_inqi_age65plus,
        date: datum.date,
        adjustment: 'Unadjusted',
      });
      newData.push({
        age_18_29:
          datum.sa_auto_inqi_age18to29 ||
          datum.sa_mtg_inqi_age18to29 ||
          datum.sa_cc_inqi_age18to29,
        age_30_44:
          datum.sa_auto_inqi_age30to44 ||
          datum.sa_mtg_inqi_age30to44 ||
          datum.sa_cc_inqi_age30to44,
        age_45_64:
          datum.sa_auto_inqi_age45to64 ||
          datum.sa_mtg_inqi_age45to64 ||
          datum.sa_cc_inqi_age45to64,
        age_65_plus:
          datum.sa_auto_inqi_age65plus ||
          datum.sa_mtg_inqi_age65plus ||
          datum.sa_cc_inqi_age65plus,
        date: datum.date,
        adjustment: 'Seasonally Adjusted',
      });
      return newData;
    }, []);

    return data.sort((a, b) => new Date(a.date) - new Date(b.date));
  },

  /* Convert Credit Tightness Index to allow filterable selection between Unadjusted and Seasonally Adjusted risk data sets (MTG/AUTO/CC) */
  cct_crti_risk_filterable(data) {
    data = data.reduce((newData, datum) => {
      newData.push({
        deep_subprime:
          datum.nsa_auto_crti_riskDeepSubprime ||
          datum.nsa_mtg_crti_riskDeepSubprime ||
          datum.nsa_cc_crti_riskDeepSubprime,
        sub_prime:
          datum.nsa_auto_crti_riskSubprime ||
          datum.nsa_mtg_crti_riskSubprime ||
          datum.nsa_cc_crti_riskSubprime,
        near_prime:
          datum.nsa_auto_crti_riskNearPrime ||
          datum.nsa_mtg_crti_riskNearPrime ||
          datum.nsa_cc_crti_riskNearPrime,
        prime:
          datum.nsa_auto_crti_riskPrime ||
          datum.nsa_mtg_crti_riskPrime ||
          datum.nsa_cc_crti_riskPrime,
        super_prime:
          datum.nsa_auto_crti_riskSuperprime ||
          datum.nsa_mtg_crti_riskSuperprime ||
          datum.nsa_cc_crti_riskSuperprime,
        date: datum.date,
        adjustment: 'Unadjusted',
      });
      newData.push({
        deep_subprime:
          datum.sa_auto_crti_riskDeepSubprime ||
          datum.sa_mtg_crti_riskDeepSubprime ||
          datum.sa_cc_crti_riskDeepSubprime,
        sub_prime:
          datum.sa_auto_crti_riskSubprime ||
          datum.sa_mtg_crti_riskSubprime ||
          datum.sa_cc_crti_riskSubprime,
        near_prime:
          datum.sa_auto_crti_riskNearPrime ||
          datum.sa_mtg_crti_riskNearPrime ||
          datum.sa_cc_crti_riskNearPrime,
        prime:
          datum.sa_auto_crti_riskPrime ||
          datum.sa_mtg_crti_riskPrime ||
          datum.sa_cc_crti_riskPrime,
        super_prime:
          datum.sa_auto_crti_riskSuperprime ||
          datum.sa_mtg_crti_riskSuperprime ||
          datum.sa_cc_crti_riskSuperprime,
        date: datum.date,
        adjustment: 'Seasonally Adjusted',
      });
      return newData;
    }, []);

    return data.sort((a, b) => new Date(a.date) - new Date(b.date));
  },

  /* Convert Credit Inquiries to allow filterable selection between Unadjusted and Seasonally Adjusted risk data sets (MTG/AUTO/CC) */
  cct_inqi_risk_filterable(data) {
    data = data.reduce((newData, datum) => {
      newData.push({
        deep_subprime:
          datum.nsa_auto_inqi_riskDeepSubprime ||
          datum.nsa_mtg_inqi_riskDeepSubprime ||
          datum.nsa_cc_inqi_riskDeepSubprime,
        sub_prime:
          datum.nsa_auto_inqi_riskSubprime ||
          datum.nsa_mtg_inqi_riskSubprime ||
          datum.nsa_cc_inqi_riskSubprime,
        near_prime:
          datum.nsa_auto_inqi_riskNearPrime ||
          datum.nsa_mtg_inqi_riskNearPrime ||
          datum.nsa_cc_inqi_riskNearPrime,
        prime:
          datum.nsa_auto_inqi_riskPrime ||
          datum.nsa_mtg_inqi_riskPrime ||
          datum.nsa_cc_inqi_riskPrime,
        super_prime:
          datum.nsa_auto_inqi_riskSuperprime ||
          datum.nsa_mtg_inqi_riskSuperprime ||
          datum.nsa_cc_inqi_riskSuperprime,
        date: datum.date,
        adjustment: 'Unadjusted',
      });
      newData.push({
        deep_subprime:
          datum.sa_auto_inqi_riskDeepSubprime ||
          datum.sa_mtg_inqi_riskDeepSubprime ||
          datum.sa_cc_inqi_riskDeepSubprime,
        sub_prime:
          datum.sa_auto_inqi_riskSubprime ||
          datum.sa_mtg_inqi_riskSubprime ||
          datum.sa_cc_inqi_riskSubprime,
        near_prime:
          datum.sa_auto_inqi_riskNearPrime ||
          datum.sa_mtg_inqi_riskNearPrime ||
          datum.sa_cc_inqi_riskNearPrime,
        prime:
          datum.sa_auto_inqi_riskPrime ||
          datum.sa_mtg_inqi_riskPrime ||
          datum.sa_cc_inqi_riskPrime,
        super_prime:
          datum.sa_auto_inqi_riskSuperprime ||
          datum.sa_mtg_inqi_riskSuperprime ||
          datum.sa_cc_inqi_riskSuperprime,
        date: datum.date,
        adjustment: 'Seasonally Adjusted',
      });
      return newData;
    }, []);

    return data.sort((a, b) => new Date(a.date) - new Date(b.date));
  },
};

export default hooks;
