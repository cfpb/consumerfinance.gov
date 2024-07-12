import EventObserver from '../utils/EventObserver';
import Highcharts from 'highcharts/highmaps';
import accessibility from 'highcharts/modules/accessibility';
import colorRange from '../utils/color-range';
import outlines from '../utils/state-outlines';
import separators from '../utils/map-separators';

accessibility( Highcharts );

Highcharts.setOptions( {
  lang: {
    thousandsSep: ','
  }
} );

class GeoMap {

  constructor(
    {
      el,
      metadata,
      data,
      color,
      desc,
      shapes,
      tooltipFormatter,
      pointDescriptionFormatter,
      seriesDescriptionFormatter,
      screenReaderSectionFormatter
    }
  ) {
    // Attach public events.
    const eventObserver = new EventObserver();
    this.addEventListener = eventObserver.addEventListener;
    this.removeEventListener = eventObserver.removeEventListener;
    this.dispatchEvent = eventObserver.dispatchEvent;
    const that = this;

    // Add the color attribute if needed so we can hook into it with the CSS.
    if ( color && el.getAttribute( 'data-chart-color' ) === null ) {
      el.setAttribute( 'data-chart-color', color );
    }

    this.lastGeoType = metadata;

    this.chartOptions = {
      chart: {
        styledMode: true,
        events: {
          afterUpdate: event => {
            that.dispatchEvent( 'afterUpdate', event );
          }
        }
      },
      credits: false,
      title: {
        text: ''
      },
      animation: {
        duration: 2000,
        easing: 'easeOutBounce'
      },
      legend: false,
      description: desc,
      mapNavigation: {
        enabled: true,
        enableMouseWheelZoom: false
      },
      accessibility: {
        exposeAsGroupOnly: true,
        enabled: true,
        keyboardNavigation: {
          enabled: true
        },
        skipNullPoints: true
      },
      tooltip: {
        animation: false,
        followPointer: false
      },
      states: {
        hover: {
          brightness: 0
        }
      },
      colorAxis: {
        dataClasses: colorRange[color],
        dataClassColor: 'category'
      },
      series: this.constructor.getSeries( data, shapes, metadata )
    };

    if ( tooltipFormatter ) {
      this.chartOptions.tooltip.useHTML = true;

      /**
       * pointDescriptionFormatter - Formatter function for tooltips.
       *
       * @returns {type} HTML string for the tooltip.
       */
      this.chartOptions.tooltip.formatter = function() {
        return tooltipFormatter( this.point, data[0].meta );
      };
    }

    if ( pointDescriptionFormatter ) {

      /**
       * pointDescriptionFormatter - Formatter function to use instead of the
       *  default for point descriptions.
       *
       * @param {type} point Highcharts point to describe
       *
       * @returns {type} String with the description of the point for a screen
       *  reader user.
       */
      this.chartOptions.pointDescriptionFormatter = function( point ) {
        return pointDescriptionFormatter( point, data[0].meta );
      };
    }

    if ( seriesDescriptionFormatter ) {

      /**
       * screenReaderSectionFormatter - Formatter function to use instead of the
       *  default for series descriptions.
       *
       * @param {type} series Highcharts series to describe
       *
       * @returns {type} String with the description of the series for a screen
       *  reader user.
       */
      this.chartOptions.seriesDescriptionFormatter = function( series ) {
        return seriesDescriptionFormatter( series );
      };
    }

    if ( screenReaderSectionFormatter ) {

      /**
       * screenReaderSectionFormatter - A formatter function to create the HTML
       *  contents of the hidden screen reader information region.
       *
       * @param {type} chart Highcharts chart object
       *
       * @returns {type} String with the HTML content of the region.
       */
      this.chartOptions.screenReaderSectionFormatter = function( chart ) {
        return screenReaderSectionFormatter( chart );
      };
    }

    // Set the chart type in the markup so CSS can pick it and be applied.
    el.classList.add( 'cfpb-chart' );
    el.setAttribute( 'data-chart-type', 'geo-map' );

    // TODO: remove when gulp build config is updated to handle spread operator.
    // eslint-disable-next-line prefer-object-spread
    this.chart = Highcharts.mapChart( el, Object.assign( {}, this.chartOptions ) );
  }

  static getSeries( data, shapes, metadata ) {
    const usMap = Highcharts.geojson( shapes );
    const borders = Highcharts.geojson( outlines, 'mapline' );
    const lines = Highcharts.geojson( separators, 'mapline' );
    const rows = data[0].data;
    const points = [];

    usMap.forEach( mapPoint => {
      if ( rows[mapPoint.properties.id] ) {
        mapPoint.name = rows[mapPoint.properties.id].name;
      } else {
        // Preserve the map point but leave its name blank if it has no data.
        mapPoint.name = '';
      }
      points.push( mapPoint );
    } );

    data = Object.keys( rows ).map( row => ( {
      fips: row,
      name: rows[row].name,

      /* Records with insufficient data are 'null' in the API.
         If the record's value is anything but a number, set it to -1. */
      value: typeof rows[row].value === 'number' ? rows[row].value * 100 : -1
    } ) );

    const stateOutlinesLayer = {
      type: 'mapline',
      name: 'Borders',
      accessibility: {
        exposeAsGroupOnly: false,
        keyboardNavigation: { enabled: false }
      },
      data: borders,
      enableMouseTracking: false,
      className: `cfpb-chart-geo-state-outline-${ metadata }`,
      id: `cfpb-chart-geo-state-outline-${ metadata }`,
      // State data comes with state outlines so remove that layer
      visible: metadata !== 'states',
      states: {
        hover: {
          enabled: false
        }
      }
    };

    const mapSeparatorsLayer = {
      type: 'mapline',
      name: 'Map separators',
      accessibility: {
        exposeAsGroupOnly: false,
        keyboardNavigation: { enabled: false }
      },
      data: lines,
      enableMouseTracking: false,
      id: 'cfpb-chart-geo-map-separators',
      className: 'cfpb-chart-geo-map-separators',
      states: {
        hover: {
          enabled: false
        }
      }
    };

    const dataLayer = {
      mapData: points,
      accessibility: { exposeAsGroupOnly: true },
      className: `cfpb-chart-geo-data-outline-${ metadata }`,
      id: `cfpb-chart-geo-data-outline-${ metadata }`,
      data: data,
      nullInteraction: true,
      joinBy: [ 'id', 'fips' ],
      states: {
        hover: {
          enabled: false
        }
      }
    };

    return [ dataLayer, mapSeparatorsLayer, stateOutlinesLayer ];
  }

  update( newOptions ) {

    if ( newOptions.data ) {
      newOptions.series = this.constructor.getSeries(
        newOptions.data,
        newOptions.shapes,
        newOptions.metadata
      );
    }

    if ( newOptions.tooltipFormatter ) {
      newOptions.tooltip = {
        useHTML: true,
        followPointer: false,
        animation: false,
        formatter: function() {
          return newOptions.tooltipFormatter(
            this.point,
            newOptions.data[0].meta
          );
        }
      };
    }

    // Merge the old chart options with the new ones
    this.chartOptions = Object.assign( this.chartOptions, newOptions );

    /* For some reason this.chart.update( this.chartOptions ) isn't working
       for updating the map series (the prior series gets merged in),
       so we remove and re-add the map layers instead before calling
       update to redraw the map. */
    if ( newOptions.needNewMapShapes ) {
      delete this.chartOptions.series;

      this.chart.get( `cfpb-chart-geo-data-outline-${ this.lastGeoType }` ).remove( false );
      this.chart.addSeries( newOptions.series[0], false );

      this.chart.get( 'cfpb-chart-geo-map-separators' ).remove( false );
      this.chart.addSeries( newOptions.series[1], false );

      this.chart.get( `cfpb-chart-geo-state-outline-${ this.lastGeoType }` ).remove( false );
      this.chart.addSeries( newOptions.series[2], false );

      this.lastGeoType = newOptions.metadata;
    }
    this.chart.update( this.chartOptions );
    this.chart.hideLoading();
  }

}

export default GeoMap;
