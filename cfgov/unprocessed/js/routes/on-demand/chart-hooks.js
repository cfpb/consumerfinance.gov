const hooks = {
  monotonicY(data) {
    return data.map((item, i) => {
      return {
        ...item,
        y: i + 1
      }
    })
  },
  enforcement_reliefTooltipFormatter() {
    const { x, y, name, relief, url } = this.points[0].point.options
    const total =
      y > 1e9
        ? `${(y / 1e9).toFixed(1)} billion`
        : `${(y / 1e6).toFixed(1)} million`
    return (
      `<div style="margin-bottom: 0.5em;"><span style="font-weight: 500">${new Date(
        x
      ).toLocaleDateString('en-US')}</span><br/>` +
      `Total relief to date: <span style="font-weight: 500">$${total}</span></div>` +
      `<a rel="noopener noreferrer" target="_blank" href="${url}" style="display: block; max-width: 200px; text-decoration-style: dotted; text-overflow: ellipsis; overflow:hidden;">${name}</a>` +
      `Relief from action: <span style="font-weight: 500">$${relief}</span>`
    )
  },

  enforcement_yAxisLabelsFormatter() {
    return `$${Math.round(this.value / 1e9)}`
  },

  enforcement_actionsTooltipFormatter() {
    const { x, y, name, url } = this.points[0].point.options
    return (
      `<div style="margin-bottom: 0.5em;"><span style="font-weight: 500">${new Date(
        x
      ).toLocaleDateString('en-US')}</span><br/>` +
      `Total actions to date: <span style="font-weight: 500">${y}</span></div>` +
      `<a rel="noopener noreferrer" target="_blank" href="${url}" style="display: block; max-width: 200px; text-decoration-style: dotted; text-overflow: ellipsis; overflow:hidden;">${name}</a>`
    )
  }
}

export default hooks
