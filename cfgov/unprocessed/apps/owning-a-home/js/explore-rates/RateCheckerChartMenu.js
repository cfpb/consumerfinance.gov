import { assign } from '../../../../js/modules/util/assign';

const STATES = {
  OPEN:   'OPEN',
  CLOSED: 'CLOSED'
};

class RateCheckerChartMenu {

  /**
   * Set the initial state value and call
   * the appropriate instantiation methods.
   * @param {object} highCharts HighCharts instance.
   */
  constructor( highCharts ) {
    this.highCharts = highCharts;
    this.state = { position: STATES.CLOSED };
    this.element = document.querySelector( '.chart-menu' );
    if ( this.element ) this._initEvents();
  }

  /**
   * Export the chart using the HighCharts API.
   * @param {string|number} exportType The type of chart.
   */
  exportChart( exportType ) {
    const highCharts = this.highCharts;

    switch ( Number( exportType ) ) {
      case 1:
        highCharts.exportChart( { type: 'image/svg+xml' } );
        break;
      case 2:
        highCharts.exportChart( { type: 'image/jpeg' } );
        break;
      case 3:
        highCharts.print();
        break;
      default:
        highCharts.exportChart();
    }
  }

  /**
   * Open the menu by setting the appropriate state.
   */
  open() {
    this._setState( { position: STATES.OPEN } );
  }

  /**
   * Close the menu by setting the appropriate state.
   */
  close() {
    this._setState( { position: STATES.CLOSED } );
  }

  /**
   * Call the appropriate methods based on the event.
   * @param {MouseEvent} event Menu click event.
   */
  onClick( event ) {
    if ( this.state.position === STATES.CLOSED ) {
      this.open();
    } else {
      this.close();
      const exportType = event.target.getAttribute( 'data-export-type' );
      if ( exportType ) this.exportChart( exportType );
    }
  }

  /**
   * Render the menu UI changes.
   * @param {object} oldState The previous state of the menu.
   * @param {object} newState The current state of the menu.
   */
  render( oldState, newState ) {
    const STATE_PREFIX = 'chart-menu__';

    this.element.classList.remove(
      STATE_PREFIX + oldState.position.toLowerCase()
    );
    this.element.classList.add(
      STATE_PREFIX + newState.position.toLowerCase()
    );
  }

  /**
   * Initialize the events for the base menu element.
   */
  _initEvents() {
    this.element.addEventListener( 'click', this.onClick.bind( this ) );
  }

  /**
   * Set the state of the RateCheckerChartMenu.
   * @param {object} state The position of the menu.
   */
  _setState( state = {} ) {
    const oldState = assign( {}, this.state );
    assign( this.state, state );
    this.render( oldState, this.state );
  }
}

RateCheckerChartMenu.STATES = STATES;

export default RateCheckerChartMenu;
