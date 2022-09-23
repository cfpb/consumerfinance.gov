/* global Chart, ChartjsPluginStacked100 */

import jsLoader from '../../modules/util/js-loader';

/*

Reimplementation of wagtailcharts {% render_charts %} tag.
Logic sourced from:

https://github.com/overcastsoftware/wagtailcharts/blob/43bdf2d2e1a54cfdacebe80417a21af65344d8e9/wagtailcharts/templates/wagtailcharts/tags/render_charts.html

*/

class ScriptLoader {
  constructor() {
    this.loaded = false;

    this.steps = [
      'wagtailcharts/js/accounting.js',
      'wagtailcharts/js/chart-types.js',
      'wagtailcharts/js/chart.js',
      'wagtailcharts/js/stacked-100.js',
      'wagtailcharts/js/chartjs-plugin-datalabels.min.js',
      function() {
        Chart.register( ChartjsPluginStacked100.default );
      },
      'wagtailcharts/js/wagtailcharts.js'
    ];
  }

  load() {
    if ( this.loaded ) return;

    this.runStep( 0 );
  }

  runStep( stepIndex ) {
    if ( stepIndex >= this.steps.length ) {
      return;
    }

    const step = this.steps[stepIndex];

    if ( typeof step === 'function' ) {
      step();
      this.runStep( stepIndex + 1 );
    } else {
      jsLoader.loadScript(
        '/static/' + step,
        this.runStep.bind( this, stepIndex + 1 )
      );
    }
  }
}

new ScriptLoader().load();
