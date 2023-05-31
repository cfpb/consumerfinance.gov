const STATE_OPEN = 'open';
const STATE_CLOSED = 'closed';

// These types should match the content inside the rate checker jinja template.
const EXPORT_TYPE_PNG = 'PNG';
const EXPORT_TYPE_SVG = 'SVG';
const EXPORT_TYPE_JPEG = 'JPEG';
const EXPORT_TYPE_PRINT = 'Print chart';

class RateCheckerChartMenu {
  /**
   * Set the initial state value and call
   * the appropriate instantiation methods.
   * @param {object} highCharts - HighCharts instance.
   */
  constructor(highCharts) {
    this.highCharts = highCharts;
    this.state = STATE_CLOSED;
    this.element = document.querySelector('.chart-menu');
    if (this.element) this._initEvents();
  }

  /**
   * Export the chart using the HighCharts API.
   * @param {string} exportType - Export type keyword.
   *                              May be an image type or print command.
   */
  exportChart(exportType) {
    const highCharts = this.highCharts;

    if (exportType === EXPORT_TYPE_PRINT) {
      highCharts.print();
    } else {
      const MIME_TYPES = {};
      MIME_TYPES[EXPORT_TYPE_PNG] = { type: 'image/png' };
      MIME_TYPES[EXPORT_TYPE_SVG] = { type: 'image/svg+xml' };
      MIME_TYPES[EXPORT_TYPE_JPEG] = { type: 'image/jpeg' };

      highCharts.exportChart(MIME_TYPES[exportType]);
    }
  }

  /**
   * Open the menu by setting the appropriate state.
   */
  open() {
    this._setState(STATE_OPEN);
  }

  /**
   * Close the menu by setting the appropriate state.
   */
  close() {
    this._setState(STATE_CLOSED);
  }

  /**
   * Call the appropriate methods based on the event.
   * @param {MouseEvent} event - Menu click event.
   */
  onClick(event) {
    if (this.state === STATE_CLOSED) {
      this.open();
    } else {
      this.close();
      const target = event.target;
      // Ensure we clicked on a <li>.
      if (target.tagName === 'LI') {
        const exportType = target.textContent;
        this.exportChart(exportType);
      }
    }
  }

  /**
   * Render the menu UI changes.
   * @param {string} oldState - The previous state of the menu.
   * @param {string} newState - The current state of the menu.
   */
  render(oldState, newState) {
    const STATE_PREFIX = 'chart-menu__';

    this.element.classList.remove(STATE_PREFIX + oldState);
    this.element.classList.add(STATE_PREFIX + newState);
  }

  /**
   * Initialize the events for the base menu element.
   */
  _initEvents() {
    this.element.addEventListener('click', this.onClick.bind(this));
  }

  /**
   * Set the state of the RateCheckerChartMenu.
   * @param {string} newState - The position of the menu.
   */
  _setState(newState) {
    const oldState = this.state;
    this.state = newState;
    this.render(oldState, newState);
  }
}

export default RateCheckerChartMenu;
