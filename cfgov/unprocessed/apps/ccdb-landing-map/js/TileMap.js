// import TileMap from 'cfpb-chart-builder/src/js/charts/TileMap';

import Highcharts from 'highcharts/highmaps';
import accessibility from 'highcharts/modules/accessibility';
import { processMapData } from 'cfpb-chart-builder/src/js/utils/process-json';

accessibility( Highcharts );

class TileMap {
  constructor( { el, description, data, metadata, title } ) {
    data = processMapData( data[0], metadata );

    const options = {
      chart: {
        marginTop: 150,
        styledMode: true
      },
      title: false,
      description: description,
      credits: false,
      legend: {
        enabled: false
      },
      tooltip: {
        enabled: false
      },
      series: [ {
        type: 'map',
        clip: false,
        dataLabels: {
          enabled: true,
          formatter: function() {
            return '<div class="highcharts-data-label-state-abbr">' +
                   this.point.name +
                   '<br /><span class=highcharts-data-label-state-value>' +
                   this.point.value + '%</span></div>';
          },
          useHTML: true
        },
        name: title,
        data: data
      } ]
    };

    return Highcharts.mapChart( el, options );
  }
}

export default TileMap;