import populations from './populations.js';

const hooks = {
  // Example transform
  monotonicY(data) {
    return data.map((item, i) => ({
      ...item,
      y: i + 1,
    }));
  },
  //Includes very janky alignment hack
  cpf_formatter() {
    let v = this.point.value;
    if (this.point.perCapita)
      v = this.point.perCapita * populations[this.point.name];
    const val = Math.round(v / 1e6);
    const digits = Math.ceil(Math.log10(val));
    return `<span style="visibility:hidden">${digits > 1 ? (digits > 2 ? 'o.' : 'o') : '.'}</span><span style="font-weight:500;">${
      this.point.name
    }</span><span style="visibility:hidden">${digits > 1 ? 'o' : ''}</span><br/><span style="font-weight:300">$${val}M</span>`;
  },

  cpf_labeller() {
    let val = this.point.value;
    if (this.point.perCapita) val *= populations[this.point.name];
    return `<b style="font-size:18px; font-weight:600">${
      this.point.label
    }</b><br/>Payments to consumers: <b>$${Math.round(val).toLocaleString(
      'en-US',
    )}</b><br/>Number of consumers: <b>${this.point.consumers.toLocaleString('en-US')}
    </b>`;
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
