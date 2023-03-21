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

const hooks = {
  // Example transform
  monotonicY(data) {
    return data.map((item, i) => ({
      ...item,
      y: i + 1,
    }));
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

  /* START of functions converting new CCT data sets for Credit Tightness Index (MTG/AUTO/CC) */

  // mtg
  cct_mtg_crti_filterable(data) {
    data = data.reduce((newData, datum) => {
      newData.push({
        high_income: datum.nsa_mtg_crti_incHigh,
        middle_income: datum.nsa_mtg_crti_incMiddle,
        moderate_income: datum.nsa_mtg_crti_incModerate,
        low_income: datum.nsa_mtg_crti_incLow,
        date: datum.date,
        adjustment: 'Unadjusted',
      });
      newData.push({
        high_income: datum.sa_mtg_crti_incHigh,
        middle_income: datum.sa_mtg_crti_incMiddle,
        moderate_income: datum.sa_mtg_crti_incModerate,
        low_income: datum.sa_mtg_crti_incLow,
        date: datum.date,
        adjustment: 'Seasonally Adjusted',
      });
      return newData;
    }, []);

    return data.sort((a, b) => new Date(a.date) - new Date(b.date));
  },

  // auto
  cct_auto_crti_filterable(data) {
    data = data.reduce((newData, datum) => {
      newData.push({
        high_income: datum.nsa_auto_crti_incHigh,
        middle_income: datum.nsa_auto_crti_incMiddle,
        moderate_income: datum.nsa_auto_crti_incModerate,
        low_income: datum.nsa_auto_crti_incLow,
        date: datum.date,
        adjustment: 'Unadjusted',
      });
      newData.push({
        high_income: datum.sa_auto_crti_incHigh,
        middle_income: datum.sa_auto_crti_incMiddle,
        moderate_income: datum.sa_auto_crti_incModerate,
        low_income: datum.sa_auto_crti_incLow,
        date: datum.date,
        adjustment: 'Seasonally Adjusted',
      });
      return newData;
    }, []);

    return data.sort((a, b) => new Date(a.date) - new Date(b.date));
  },

  // cc
  cct_cc_crti_filterable(data) {
    data = data.reduce((newData, datum) => {
      newData.push({
        high_income: datum.nsa_cc_crti_incHigh,
        middle_income: datum.nsa_cc_crti_incMiddle,
        moderate_income: datum.nsa_cc_crti_incModerate,
        low_income: datum.nsa_cc_crti_incLow,
        date: datum.date,
        adjustment: 'Unadjusted',
      });
      newData.push({
        high_income: datum.sa_cc_crti_incHigh,
        middle_income: datum.sa_cc_crti_incMiddle,
        moderate_income: datum.sa_cc_crti_incModerate,
        low_income: datum.sa_cc_crti_incLow,
        date: datum.date,
        adjustment: 'Seasonally Adjusted',
      });
      return newData;
    }, []);

    return data.sort((a, b) => new Date(a.date) - new Date(b.date));
  },

  /* END of functions converting new CCT data sets for Credit Tightness Index (MTG/AUTO/CC) */

  /* START of functions converting new CCT data sets for Credit Inquiries (MTG/AUTO/CC) */

  // mtg
  cct_mtg_inqi_filterable(data) {
    data = data.reduce((newData, datum) => {
      newData.push({
        high_income: datum.nsa_mtg_inqi_incHigh,
        middle_income: datum.nsa_mtg_inqi_incMiddle,
        moderate_income: datum.nsa_mtg_inqi_incModerate,
        low_income: datum.nsa_mtg_inqi_incLow,
        date: datum.date,
        adjustment: 'Unadjusted',
      });
      newData.push({
        high_income: datum.sa_mtg_inqi_incHigh,
        middle_income: datum.sa_mtg_inqi_incMiddle,
        moderate_income: datum.sa_mtg_inqi_incModerate,
        low_income: datum.sa_mtg_inqi_incLow,
        date: datum.date,
        adjustment: 'Seasonally Adjusted',
      });
      return newData;
    }, []);

    return data.sort((a, b) => new Date(a.date) - new Date(b.date));
  },

  // auto
  cct_auto_inqi_filterable(data) {
    data = data.reduce((newData, datum) => {
      newData.push({
        high_income: datum.nsa_auto_inqi_incHigh,
        middle_income: datum.nsa_auto_inqi_incMiddle,
        moderate_income: datum.nsa_auto_inqi_incModerate,
        low_income: datum.nsa_auto_inqi_incLow,
        date: datum.date,
        adjustment: 'Unadjusted',
      });
      newData.push({
        high_income: datum.sa_auto_inqi_incHigh,
        middle_income: datum.sa_auto_inqi_incMiddle,
        moderate_income: datum.sa_auto_inqi_incModerate,
        low_income: datum.sa_auto_inqi_incLow,
        date: datum.date,
        adjustment: 'Seasonally Adjusted',
      });
      return newData;
    }, []);

    return data.sort((a, b) => new Date(a.date) - new Date(b.date));
  },

  // cc
  cct_cc_inqi_filterable(data) {
    data = data.reduce((newData, datum) => {
      newData.push({
        high_income: datum.nsa_cc_inqi_incHigh,
        middle_income: datum.nsa_cc_inqi_incMiddle,
        moderate_income: datum.nsa_cc_inqi_incModerate,
        low_income: datum.nsa_cc_inqi_incLow,
        date: datum.date,
        adjustment: 'Unadjusted',
      });
      newData.push({
        high_income: datum.sa_cc_inqi_incHigh,
        middle_income: datum.sa_cc_inqi_incMiddle,
        moderate_income: datum.sa_cc_inqi_incModerate,
        low_income: datum.sa_cc_inqi_incLow,
        date: datum.date,
        adjustment: 'Seasonally Adjusted',
      });
      return newData;
    }, []);

    return data.sort((a, b) => new Date(a.date) - new Date(b.date));
  },

  /* END of functions converting new CCT data sets for Credit Inquiries (MTG/AUTO/CC) */
};

export default hooks;
