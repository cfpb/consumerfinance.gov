'use strict';

const utils = require( '../utils' );

const defaultActionCreators = () => {

  const actions = {

    /**
     * setGeo - Sets geographic location's info
     *
     * @param {String} geoId   ID of location
     * @param {String} geoName Name of location
     * @param {String} geoType Type of location (state, metro, county)
     *
     * @returns {Object} Action to set geo
     */
    setGeo: ( geoId, geoName, geoType ) => ( {
      type: 'SET_GEO',
      geo: {
        type: geoType,
        id: geoId,
        name: geoName
      }
    } ),

    /**
     * clearGeo - Clears geographic location's info
     *
     * @returns {Object} Action to clear geo
     */
    clearGeo: () => ( {
      type: 'CLEAR_GEO'
    } ),

   /**
    * updateChart - Action dispatched to redraw the chart/map
    *
    * @param {String} geoId   ID of location
    * @param {String} geoName Name of location
    * @param {String} geoType Type of location (state, metro, county)
    * @param {Boolean} includeComparison Include national comparison?
    *
    * @returns {Object} Action to update chart
    */
    updateChart: ( geoId, geoName, geoType, includeComparison ) => {
      var action = {
        type: 'UPDATE_CHART',
        geo: {
          id: geoId,
          name: geoName
        },
        includeComparison
      };
      if ( geoType ) {
        action.geo.type = geoType;
      }
      return action;
    },

  /**
   * updateNational - Action dispatched when the national comparison is toggled
   *
   * @param {Boolean} includeComparison Include national comparison?
   *
   * @returns {Object} Action to include the national data in chart
   */
    updateNational: includeComparison => {
      var action = {
        type: 'UPDATE_CHART',
        includeComparison
      };
      return action;
    },

    /**
     * updateDate - Action dispatched when the month/year is changed
     *
     * @param {String} date Date in format 2010-01
     *
     * @returns {Object} Action to update the data viz's date
     */
    updateDate: date => ( {
      type: 'UPDATE_DATE',
      date: date
    } ),

    /**
     * requestCounties - Action indicating county names are being downloaded.
     *
     * @returns {Object} Action with county loading state
     */
    requestCounties: () => ( {
      type: 'REQUEST_COUNTIES',
      isLoadingCounties: true
    } ),

    /**
     * requestMetros - Action indicating metro names are being downloaded.
     *
     * @returns {Object} Action with metro loading state
     */
    requestMetros: () => ( {
      type: 'REQUEST_METROS',
      isLoadingMetros: true
    } ),

    /**
     * requestNonMetros - Action indicating non metro names are being downloaded
     *
     * @returns {Object} Action with non metro loading state
     */
    requestNonMetros: () => ( {
      type: 'REQUEST_NON_METROS',
      isLoadingNonMetros: true
    } ),

    /**
     * fetchNonMetros - Creates async action to fetch list of non-metros.
     *
     * @param {String} nonMetroState Two-letter U.S. state abbreviation.
     * @param {Boolean} includeComparison Include national comparison?
     *
     * @returns {Function} Thunk called with non metros
     */
    fetchNonMetros: ( nonMetroState, includeComparison ) => dispatch => {
      dispatch( actions.requestNonMetros() );
      return utils.getNonMetroData( data => {
        let nonMetros = data.filter( nonMetro => nonMetro.valid );
        let currStateIndex = 0;
        nonMetros.forEach( ( nonMetro, i ) => {
          if ( nonMetro.abbr === nonMetroState ) {
            currStateIndex = i;
          }
        } );
        // Alphabetical order
        nonMetros = nonMetros.sort( ( a, b ) => a.name < b.name ? -1 : 1 );
        dispatch( actions.setNonMetros( nonMetros ) );
        dispatch( actions.setGeo( nonMetros[currStateIndex].fips, nonMetros[currStateIndex].name, 'non-metro' ) );
        dispatch( actions.updateChart( nonMetros[currStateIndex].fips, nonMetros[currStateIndex].name, 'non-metro', includeComparison ) );
        return nonMetros;
      } );
    },

    /**
     * setMetros - New metros to store in state.
     *
     * @param {Array} metros List of metros.
     * @returns {Object} Action with new metros.
     */
    setMetros: metros => ( {
      type: 'SET_METROS',
      metros: metros
    } ),

    /**
     * setNonMetros - New non-metros to store in state.
     *
     * @param {Array} nonMetros List of non-metros.
     * @returns {Object} Action with new non-metros.
     */
    setNonMetros: nonMetros => ( {
      type: 'SET_NON_METROS',
      nonMetros: nonMetros
    } ),

    /**
     * setCounties - New counties to store in state.
     *
     * @param {Array} counties List of counties.
     * @returns {Object} Action with new counties.
     */
    setCounties: counties => ( {
      type: 'SET_COUNTIES',
      counties: counties
    } ),

    /**
     * startLoading - Set global loading state for the app.
     *
     * @returns {Object} Action indicating the app is loading.
     */
    startLoading: () => ( {
      type: 'START_LOADING',
      isLoading: true
    } ),

    /**
     * stopLoading - Set global loading state for the app.
     *
     * @returns {Object} Action indicating the app is not loading.
     */
    stopLoading: () => ( {
      type: 'STOP_LOADING',
      isLoading: false
    } )
  };

  return actions;

};

module.exports = defaultActionCreators;
