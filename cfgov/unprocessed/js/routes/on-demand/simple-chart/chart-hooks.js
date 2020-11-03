const hooks = {
  monotonicY(data) {
    return data.map((item, i) => {
      return {
        ...item,
        y: i + 1
      }
    })
  },

  enforcement_barCount(data) {
    const years = {}
    data.forEach(d => {
      const year = new Date(d.x).getFullYear()
      if (years[year]) years[year]++
      else years[year] = 1
    })
    return Object.keys(years)
      .sort()
      .map(k => {
        return { name: k, y: years[k] }
      })
  },

  enforcement_barCategories(data) {
    return data.map(d => d.name)
  },

  enforcement_reliefTooltipFormatter() {
    const { x, y, name, relief, url } = this.points[0].point.options
    return (
      `<div style="margin-bottom: 0.5em;"><span style="font-weight: 500">${new Date(
        x
      ).toLocaleDateString('en-US', { dateStyle: 'medium' })}</span><br/>` +
      `Total relief to date: <span style="font-weight: 500">$${y.toLocaleString()}</span></div>` +
      `<a rel="noopener noreferrer" target="_blank" href="${url}" style="display: block; max-width: 285px; text-decoration: underline; text-decoration-style:dotted; text-overflow: ellipsis; overflow:hidden;">${name}</a>` +
      `Relief from action: <span style="font-weight: 500">$${relief}</span>`
    )
  },

  enforcement_yAxisLabelsFormatter() {
    return `$${Math.round(this.value / 1e9)}B`
  },

  enforcement_actionsTooltipFormatter() {
    const { x, y, name, url } = this.points[0].point.options
    return (
      `<div style="margin-bottom: 0.5em;"><span style="font-weight: 500">${new Date(
        x
      ).toLocaleDateString('en-US')}</span><br/>` +
      `Total actions to date: <span style="font-weight: 500">${y}</span></div>` +
      `<a rel="noopener noreferrer" target="_blank" href="${url}" style="display: block; max-width: 180px; text-decoration: underline; text-decoration-style:dotted; text-overflow: ellipsis; overflow:hidden;">${name}</a>`
    )
  },

  enforcement_barTooltipFormatter() {
    const { y, name } = this.points[0].point.options
    return (
      `<span style="font-weight: 500">${name}</span><br/>` +
      `Total enforcement actions: <span style="font-weight: 500">${y}</span>`
    )
  }
}

export default hooks
