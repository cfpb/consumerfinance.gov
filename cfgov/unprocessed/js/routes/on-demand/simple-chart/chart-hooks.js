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

  cct_age(d, age) {
    return d.filter((v) => v.age__group === age);
  },

  cct_age_yoy(d, age) {
    d[age].map((v) => {
      return {
        x: v[0],
        percent: v[1] * 100,
      };
    });
  },

  getDateString(x) {
    return new Date(x).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      timeZone: 'UTC',
    });
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
};

export default hooks;
