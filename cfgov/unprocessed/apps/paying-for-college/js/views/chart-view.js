import {
  getExpensesValue,
  getFinancialValue,
  getSchoolCohortValue,
  getSchoolValue,
  getStateValue
} from '../dispatchers/get-model-values.js';
import Highcharts from 'highcharts/highstock';
import accessibility from 'highcharts/modules/accessibility';
import more from 'highcharts/highcharts-more';
import numberToMoney from 'format-usd';
import patternFill from "highcharts/modules/pattern-fill";
import { updateState } from '../dispatchers/update-state.js';

// curlies in strings is a way of formatting Highcharts labels
/* eslint-disable no-template-curly-in-string */

more( Highcharts );
patternFill(Highcharts);

const columnChartOpts = {
  _meterChartBtns: null,

  chart: {
    type: 'column',
    marginRight: 250
  },
  legend: {
    layout: 'vertical',
    backgroundColor: '#FFFFFF',
    floating: true,
    align: 'right',
    itemMarginTop: 10,
    itemStyle: {
      fontSize: '1.2em',
      lineHeight: '3em'
    },
    verticalAlign: 'middle',
    x: -90,
    y: -45,
    labelFormatter: function() {
      return this.name;
    }
  },
  title: false,
  tooltip: false,
  xAxis: {
    categories: [
      '10 year period',
      '25 year period'
    ]
  },
  yAxis: {
    min: 0,
    max: 60000,
    title: '',
    stackLabels: {
      enabled: true,
      format: '${total:,.0f}'
    }
  },
  series: [ {
    name: 'Interest',
    data: [ 0, 0 ],
    color: '#ffe1b9'
  }, {
    name: 'Principal',
    data: [ 0, 0 ],
    color: '#ff9e1b'
  } ],
  plotOptions: {
    series: {
      pointPadding: 0.1,
      dataLabels: {
        enabled: false
      }
    },
    column: {
      stacking: 'normal'
    }
  }
};

const meterOpts = {
  chart: {
    type: 'gauge',
    plotBorderWidth: 0,
    plotBackgroundColor: 'none',
    plotBackgroundImage: null,
    height: 300,
    styledMode: false
  },

  title: {
    text: ''
  },

  pane: [ {
    startAngle: -90,
    endAngle: 90,
    background: null,
    center: [ '50%', '90%' ],
    size: 275
  } ],

  exporting: {
    enabled: false
  },

  tooltip: false,

  yAxis: [ {
    min: 0,
    max: 180,
    lineWidth: 0,
    minorTickInterval: null,
    tickPosition: 'inside',
    tickPositions: [],
    labels: 'none',
    plotBands: [ {
      from: 0,
      to: 60,
      color: '#d14124',
      innerRadius: '90%',
      outerRadius: '110%',
      label: {
        text: '<strong>MIN</strong>',
        align: 'left',
        x: 80,
        y: 75
      }
    }, {
      from: 60,
      to: 120,
      color: '#ff9e1b',
      innerRadius: '90%',
      outerRadius: '110%',
      label: {
        text: '<strong>MEDIAN</strong>',
        align: 'center',
        x: 135,
        y: -15
      }
    }, {
      from: 120,
      to: 180,
      color: '#257675',
      innerRadius: '90%',
      outerRadius: '110%',
      label: {
        text: '<strong>MAX</strong>',
        align: 'right',
        x: -60,
        y: 75
      }
    } ],
    pane: 0,
    title: {
      text: '',
      y: -40
    }
  } ],

  plotOptions: {
    gauge: {
      dataLabels: {
        enabled: false
      },
      dial: {
        radius: '100%'
      }
    }
  },

  series: [ {
    name: '',
    data: [ 50 ],
    yAxis: 0
  } ]

};

const horizontalBarOpts = {
  chart: {
    type: 'bar',
    marginTop: 75,
    height: 250
  },
  title: false,
  subtitle: false,
  xAxis: {
    categories: [],
    title: {
      text: null
    }
  },
  yAxis: {
    min: 0,
    max: 45000,
    stackLabels: {
      enabled: true,
      format: 'Your funding<br>${total:,.0f}',
      align: 'right'
    },
    plotLines: [ {
      color: 'red',
      width: 2,
      value: 25896,
      zIndex: 4,
      label: {
        align: 'center',
        text: 'Cost of Attendance<br>$25,896',
        rotation: 0,
        x: 0,
        y: -25
      }
    } ],
    title: false,
    labels: {
      overflow: 'justify'
    }
  },
  tooltip: false,
  plotOptions: {
    bar: {
      dataLabels: {
        enabled: false
      }
    },
    series: {
      stacking: 'normal'
    }
  },
  legend: {
    enabled: false,
    layout: 'vertical',
    align: 'right',
    verticalAlign: 'top',
    x: -40,
    y: 80,
    floating: true,
    borderWidth: 1,
    backgroundColor: '#FFFFFF',
    shadow: true
  },
  credits: {
    enabled: false
  },
  series: [ {
    data: [ 10000 ]
  } ]
};

const compareCostOfBorrowingOpts = {
  yAxis: {
    max: 60000
  },
  series: [ {
    name: 'Interest',
    data: [ 6448, 17506 ],
    color: '#ffe1b9'
  }, {
    name: 'Principal',
    data: [ 30000, 30000 ],
    color: '#ff9e1b'
  } ]
};

const costOfBorrowingOpts = {
  chart: {
    type: 'bar',
    marginTop: 75,
    height: 350,
  },
  tooltip: false,
  title: false,
  legend: {
    enabled: true,
    align: 'left',
    floating: true,
    itemMarginTop: 5,
    itemMarginBottom: 5,
    itemStyle: {
      fontSize: '14px',
      fontWeight: '100'
    },
    layout: 'vertical',
    symbolHeight: 14,
    symbolWidth: 14,
    symbolRadius: 0,
    useHTML: true,
    verticalAlign: 'top',
    x: -10
  },
  xAxis: {
    categories: ['']
  },
  yAxis: {
    title: {
      text: 'Dollars'
    }
  },
  plotOptions: {
    series: {
      stacking: 'normal'
    }
  },
  series: [ {
    name: 'Estimated total interest: <strong>$5,000</strong>',
    pointWidth: 60,
    data: [ 10000 ],
    color: '#ff9e1b'
  }, {
    name: 'Estimated total borrowed: <strong>$55,000</strong>',
    pointWidth: 60,
    data: [ 40000 ],
    color: '#ffe1b9'
  } ]
};

const makePlanOpts = {
  series: [ {
    color: '#addc91'
  } ]
};

const maxDebtOpts = {
  chart: {
    type: 'bar',
    marginTop: 75,
    height: 350
  },
  title: false,
  subtitle: false,
  xAxis: {
    categories: [''],
    title: {
      text: null
    }
  },
  yAxis: {
    min: 0,
    max: 45000,
    stackLabels: {
      enabled: false
    },
    title: false,
    labels: {
      overflow: 'justify'
    }
  },
  tooltip: false,
  plotOptions: {
    bar: {
      dataLabels: {
        enabled: false
      },
      groupPadding: .001
    }
  },
  legend: {
    enabled: false,
  },
  credits: {
    enabled: false
  },
  series: [ {
    data: [ 43000 ],
    pointWidth: 60,
    color: '#ff9e1b'
  },{
    data: [ 35000 ],
    pointWidth: 60,
    color: {
      pattern: {
        path: `M -1,11 l11,-11 M -2 2 l3,-3 M 8, 12 l3, -3`,
        width: 10,
        height: 10,
        stroke: 1,
        color: '#fff',
        backgroundColor: '#20aa3f',
        opacity: .9,
        patternTransform: 'scale(.75)'
      }
    }
  }]
};

const affordingOpts = {
  chart: {
    type: 'bar',
    marginTop: 100,
    height: 450,
  },
  tooltip: false,
  title: false,
  legend: {
    enabled: true,
    align: 'left',
    floating: true,
    itemMarginTop: 5,
    itemMarginBottom: 5,
    itemStyle: {
      fontSize: '14px',
      fontWeight: '100'
    },
    layout: 'vertical',
    symbolHeight: 14,
    symbolWidth: 14,
    symbolRadius: 0,
    useHTML: true,
    verticalAlign: 'top',
    x: -10
  },
  xAxis: {
    categories: ['']
  },
  yAxis: {
    title: {
      text: 'Dollars'
    }
  },
  plotOptions: {
    series: {
      stacking: 'normal'
    }
  },
  series: [ {
    name: 'Estimated monthly loan payment: <strong>$524</strong>',
    pointWidth: 60,
    data: [ 524 ],
    color: '#ffe1b9',
    stack: 'costs'
  }, {
    name: 'Average monthly expenses: <strong>$2,246</strong>',
    pointWidth: 60,
    data: [ 2246 ],
    color: '#ff9e1b',
    stack: 'costs'
  }, {
    name: 'Monthly median salary: <strong>$4,357</strong>',
    pointWidth: 60,
    data: [ 4357 ],
    color: {
      pattern: {
             path: `M -1,11 l11,-11 M -2 2 l3,-3 M 8, 12 l3, -3`,
           width: 10,
           height: 10,
           stroke: 1,
           color: '#fff',
           backgroundColor: '#20aa3f',
           opacity: .9,
           patternTransform: 'scale(.75)'
      }
    },
    stack: 'salary'
  }]
};

const gradMeterOpts = {};

const repaymentMeterOpts = {};

const chartView = {
  costOfBorrowingElem: null,
  compareCostElem: null,
  meterElems: null,
  makePlanElem: null,
  maxDebtElem: null,
  affordingElem: null,
  gradMeterElem: null,
  repaymentMeterElem: null,
  costOfBorrowingChart: null,
  compareCostOfBorrowingChart: null,
  makePlanChart: null,
  maxDebtChart: null,
  affordingChart: null,
  gradMeterChart: null,
  repaymentMeterChart: null,

  init: body => {
    chartView._meterChartBtns = body.querySelectorAll( '.school-results_cohort-buttons input.a-radio' );
    chartView.costOfBorrowingElem = body.querySelector( '#cost-of-borrowing_chart' );
    chartView.compareCostElem = body.querySelector( '#compare-cost-of-borrowing_chart' );
    chartView.makePlanElem = body.querySelector( '#make-a-plan_chart' );
    chartView.maxDebtElem = body.querySelector( '#max-debt-guideline_chart' );
    chartView.affordingElem = body.querySelector( '#affording-your-loans_chart' );
    chartView.gradMeterElem = body.querySelector( '#school-results_grad-meter' );
    chartView.repaymentMeterElem = body.querySelector( '#school-results_repayment-meter' );

    _addRadioListeners();

    // Set initial buttons
    document.querySelector( '#graduation-rate_us' ).checked = true;
    document.querySelector( '#repayment-rate_us' ).checked = true;

    accessibility( Highcharts );

    Highcharts.setOptions( {
      lang: {
        rangeSelectorZoom: '',
        thousandsSep: ','
      }
    } );

    chartView.costOfBorrowingChart = Highcharts.chart(
      chartView.costOfBorrowingElem,
      { ...costOfBorrowingOpts }
    );

    chartView.compareCostOfBorrowingChart = Highcharts.chart(
      chartView.compareCostElem,
      { ...columnChartOpts, ...compareCostOfBorrowingOpts }
    );

    chartView.makePlanChart = Highcharts.chart(
      chartView.makePlanElem,
      { ...horizontalBarOpts, ...makePlanOpts }
    );

    chartView.maxDebtChart = Highcharts.chart(
      chartView.maxDebtElem,
      { ...maxDebtOpts }
    );

    chartView.maxDebtChart.debtText = chartView.maxDebtChart.renderer.text(
          'Estimated total debt at graduation: ',
          60,
          90 )
          .attr({
            zIndex: 5
          }).css({
            'fontSize':'14px'
          })
          .add();
    chartView.maxDebtChart.salaryText = chartView.maxDebtChart.renderer.text(
          'Estimated total debt at graduation: ',
          60,
          90 )
          .attr({
            zIndex: 5
          }).css({
            'fontSize':'14px'
          })
          .add();

    chartView.affordingChart = Highcharts.chart(
      chartView.affordingElem,
      { ...affordingOpts }
    );

    chartView.gradMeterChart = Highcharts.chart(
      chartView.gradMeterElem,
      { ...meterOpts, ...gradMeterOpts }
    );

    chartView.repaymentMeterChart = Highcharts.chart(
      chartView.repaymentMeterElem,
      { ...meterOpts, ...repaymentMeterOpts }
    );

  },

  updateCostOfBorrowingChart: () => {
    const totalBorrowingAtGrad = getFinancialValue( 'debt_totalAtGrad' );
    const borrowedString = numberToMoney( { amount: totalBorrowingAtGrad, decimalPlaces: 0 } );
    const interest10years = getFinancialValue( 'debt_tenYearInterest' );
    const interestString = numberToMoney( { amount: interest10years, decimalPlaces: 0 } );

    chartView.costOfBorrowingChart.yAxis[0].update( {
      max: Math.floor( getFinancialValue( 'debt_tenYearTotal' ) * 1.10 )
    } );
    chartView.costOfBorrowingChart.series[0].update( {
        data: [ interest10years ],
        name: 'Estimated total interest: <strong>' + interestString + '</strong>'
      } );
    chartView.costOfBorrowingChart.series[1].update({
        data: [ totalBorrowingAtGrad ],
        name: 'Estimated total borrowed: <strong>' + borrowedString + '</strong>'
      } );
  },

  updateMakePlanChart: () => {
    const totalCosts = getFinancialValue( 'total_costs' );
    const totalFunding = getFinancialValue( 'total_funding' );
    const max = Math.max( totalCosts * 1.1, totalFunding * 1.1 );
    const text = 'Your costs<br>' + numberToMoney( { amount: totalCosts, decimalPlaces: 0 } );

    chartView.makePlanChart.yAxis[0].update( {
      max: max,
      plotLines: [ {
        color: 'red',
        width: 2,
        value: totalCosts,
        zIndex: 4,
        label: {
          align: 'center',
          text: text,
          rotation: 0,
          x: 0,
          y: -25
        }
      } ]
    } );
    chartView.makePlanChart.series[0].setData( [ totalFunding ] );
  },

  updateMaxDebtChart: () => {
    const totalDebt = getFinancialValue( 'debt_totalAtGrad' );
    const debtString = numberToMoney( { amount: totalDebt, decimalPlaces: 0 }  );
    const salary = getFinancialValue( 'salary_annual' );
    const salaryString = numberToMoney( { amount: salary, decimalPlaces: 0 } );
    const max = Math.max( totalDebt * 1.1, salary * 1.1 );

    chartView.maxDebtChart.yAxis[0].update( {
      min: 0,
      max: max 
    } );

    chartView.maxDebtChart.series[0].setData( [ totalDebt ] );

    chartView.maxDebtChart.series[1].setData( [ salary ] );

    chartView.maxDebtChart.salaryText.destroy();
    chartView.maxDebtChart.debtText.destroy();

    chartView.maxDebtChart.debtText = chartView.maxDebtChart.renderer.text(
          'Estimated total debt at graduation: <strong>' + debtString + '</strong>',
          60,
          90 )
          .attr({
            zIndex: 5
          }).css({
            'fontSize':'14px'
          })
          .add();

    chartView.maxDebtChart.salaryText = chartView.maxDebtChart.renderer.text(
        'Estimated salary at graduation: <strong>' + salaryString + '</strong>',
        60,
        210 )
        .attr({
          zIndex: 5
        }).css({
          'fontSize':'14px'
        })
      .add()
  },

  updateAffordingChart: () => {
    const monthlyExpenses = getExpensesValue( 'total_expenses' );
    const expensesString = numberToMoney( { amount: monthlyExpenses, decimalPlaces: 0 } );
    const monthlyPayment = getFinancialValue( 'debt_tenYearMonthly' );
    const paymentString = numberToMoney( { amount: monthlyPayment, decimalPlaces: 0 } );
    const monthlySalary = getFinancialValue( 'salary_monthly' );
    const salaryString = numberToMoney( { amount: monthlySalary, decimalPlaces: 0 } );

    const max = Math.max( monthlySalary * 1.1, ( monthlyExpenses + monthlyPayment ) * 1.1 );
    const text = 'Monthly Salary<br>' + numberToMoney( { amount: monthlySalary, decimalPlaces: 0 } );

    chartView.affordingChart.yAxis[0].update( {
      min: 0,
      max: max
    } );

    chartView.affordingChart.series[0].update( {
        data: [ monthlyPayment ],
        name: 'Estimated monthly loan payment: <strong>' + paymentString + '</strong>'
      } );
    chartView.affordingChart.series[1].update({
        data: [ monthlyExpenses ],
        name: 'Average monthly expenses: <strong>' + expensesString + '</strong>'
      } );
    chartView.affordingChart.series[2].update({
        data: [ monthlySalary ],
        name: 'Monthly median salary: <strong>' + salaryString + '</strong>'
      } );
  },

  updateGradMeterChart: () => {
    let cohort = getStateValue( 'gradMeterCohort' );
    if ( !cohort ) {
      cohort = 'cohortRankByHighestDegree';
    }
    const cohortGradRate = getSchoolCohortValue( cohort, 'grad_rate' );
    if ( cohortGradRate ) {
      let percentile = cohortGradRate.percentile_rank;

      if ( percentile <= 33 ) {
        updateState.byProperty( 'gradMeterThird', 'bottom third' );
        updateState.byProperty( 'rategraduationrange', 'low' );
      } else if ( percentile <= 66 ) {
        updateState.byProperty( 'gradMeterThird', 'middle third' );
        updateState.byProperty( 'rategraduationrange', 'medium' );
      } else {
        updateState.byProperty( 'gradMeterThird', 'top third' );
        updateState.byProperty( 'rategraduationrange', 'high' );
      }

      // Percentile works along a 180-degree axis:
      percentile = percentile / 100 * 180;
      chartView.gradMeterChart.series[0].setData( [ percentile ] );
    } else {
      updateState.byProperty( 'gradMeterThird', '' );
    }
  },

  updateRepaymentMeterChart: () => {
    let cohort = getStateValue( 'repayMeterCohort' );
    if ( !cohort ) {
      cohort = 'cohortRankByHighestDegree';
    }
    const cohortRepayRate = getSchoolCohortValue( cohort, 'repay_3yr' );
    if ( cohortRepayRate ) {
      const percentile = cohortRepayRate.percentile_rank;

      if ( percentile <= 33 ) {
        updateState.byProperty( 'repayMeterThird', 'bottom third' );
        updateState.byProperty( 'raterepay3yrrange', 'low' );
      } else if ( percentile <= 66 ) {
        updateState.byProperty( 'repayMeterThird', 'middle third' );
        updateState.byProperty( 'raterepay3yrrange', 'medium' );
      } else {
        updateState.byProperty( 'repayMeterThird', 'top third' );
        updateState.byProperty( 'raterepay3yrrange', 'high' );
      }

      // Percentile works along a 180-degree axis:
      const arc = percentile / 100 * 180;
      chartView.repaymentMeterChart.series[0].setData( [ arc ] );
    }
  }
};

/**
 * Listen for radio button clicks.
 */
function _addRadioListeners() {
  chartView._meterChartBtns.forEach( elem => {
    elem.addEventListener( 'click', _handleRadioClicks );
  } );
}

/**
 * @param {MouseEvent} event - The click event object.
 */
function _handleRadioClicks( event ) {
  const target = event.target;
  const cohort = target.value;
  const graph = target.getAttribute( 'name' ).replace( /-/g, '' );
  const handlers = {
    repaymentratemeterselector: {
      'function': chartView.updateRepaymentMeterChart,
      'stateProp': 'repayMeterCohort',
      'cohortName': 'repayMeterCohortName'
    },
    graduationratemeterselector: {
      'function': chartView.updateGradMeterChart,
      'stateProp': 'gradMeterCohort',
      'cohortName': 'gradMeterCohortName'
    }
  };
  const names = {
    cohortRankByHighestDegree: 'U.S.',
    cohortRankByState: getSchoolValue( 'stateName' ),
    cohortRankByControl: getSchoolValue( 'control' )
  };

  updateState.byProperty( handlers[graph].cohortName, names[cohort] );
  updateState.byProperty( handlers[graph].stateProp, cohort );
  handlers[graph].function();
}

export {
  chartView
};
