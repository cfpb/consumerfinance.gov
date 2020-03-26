import accessibility from 'highcharts/modules/accessibility';
import Highcharts from 'highcharts/highstock';
import more from 'highcharts/highcharts-more';
import numberToMoney from 'format-usd';
import { getExpensesValue, getFinancialValue, getSchoolValue } from '../dispatchers/get-model-values.js';

// curlies in strings is a way of formatting Highcharts labels
/* eslint-disable no-template-curly-in-string */

more( Highcharts );

const columnChartOpts = {
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
  tooltip: {
    pointFormat: '${point.y:,.0f}'
  },
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
    center: [ '50%', '90%' ]
  } ],

  exporting: {
    enabled: false
  },

  tooltip: {
    enabled: false
  },

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
        x: 120,
        y: 65
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
        x: 140,
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
        x: -100,
        y: 65
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
      format: 'Total funding<br>${total:,.0f}',
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
  tooltip: {
    format: '${total:,.0f}'
  },
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
  series: [ {
    name: 'Interest',
    data: [ 0, 0 ],
    color: '#ffe1b9'
  }, {
    name: 'Amount borrowed',
    data: [ 1, 1 ],
    color: '#ff9e1b'
  } ]
};

const makePlanOpts = {

};

const maxDebtOpts = {
  marginRight: 30,
  yAxis: {
    min: 0,
    max: 45000,
    stackLabels: {
      enabled: true,
      format: '',
      align: 'right',
      x: 10
    },
    plotLines: [ {
      color: 'red',
      width: 2,
      value: 100,
      zIndex: 4,
      label: {
        align: 'center',
        text: '',
        rotation: 0,
        x: 0,
        y: -40
      }
    } ],
    title: false,
    labels: {
      overflow: 'justify'
    }
  },
  series: [ {
    color: '#ff9e1b'
  } ]
};

const affordingOpts = {
  marginRight: 30,
  yAxis: {
    min: 0,
    max: 50000,
    plotLines: [ {
      color: 'red',
      width: 2,
      value: 100,
      zIndex: 4,
      label: {
        align: 'center',
        text: '',
        rotation: 0,
        x: 0,
        y: -40
      }
    } ]
  },
  legend: {
    enabled: true,
    layout: 'vertical',
    align: 'left',
    verticalAlign: 'top',
    x: 20,
    y: -5,
    floating: true,
    borderWidth: 1,
    backgroundColor: '#FFFFFF',
    shadow: true
  },
  series: [ {
    data: [ 500 ],
    name: 'Monthly loan payment',
    color: '#ffe1b9'
  }, {
    data: [ 10000 ],
    name: 'Monthly living expenses',
    color: '#ff9e1b'
  } ]
};

const gradMeterOpts = {

};

const repaymentMeterOpts = {

};

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
    chartView.costOfBorrowingElem = body.querySelector( '#cost-of-borrowing_chart' );
    chartView.compareCostElem = body.querySelector( '#compare-cost-of-borrowing_chart' );
    chartView.makePlanElem = body.querySelector( '#make-a-plan_chart' );
    chartView.maxDebtElem = body.querySelector( '#max-debt-guideline_chart' );
    chartView.affordingElem = body.querySelector( '#affording-your-loans_chart' );
    chartView.gradMeterElem = body.querySelector( '#school-results_grad-meter' );
    chartView.repaymentMeterElem = body.querySelector( '#school-results_repayment-meter' );

    accessibility( Highcharts );

    Highcharts.setOptions( {
      lang: {
        rangeSelectorZoom: '',
        thousandsSep: ','
      }
    } );

    chartView.costOfBorrowingChart = Highcharts.chart(
      chartView.costOfBorrowingElem,
      { ...columnChartOpts, ...costOfBorrowingOpts }
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
      { ...horizontalBarOpts, ...maxDebtOpts }
    );

    chartView.affordingChart = Highcharts.chart(
      chartView.affordingElem,
      { ...horizontalBarOpts, ...affordingOpts }
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
    const totalBorrowingAtGrad = getFinancialValue( 'total_borrowingAtGrad' );
    const interest10years = getFinancialValue( 'debt_tenYearInterest' );
    const interest25years = getFinancialValue( 'debt_twentyFiveYearInterest' );

    chartView.costOfBorrowingChart.yAxis[0].update( {
      max: Math.floor( getFinancialValue( 'debt_twentyFiveYearTotal' ) * 1.10 )
    } );
    chartView.costOfBorrowingChart.series[0].setData( [ interest10years, interest25years ] );
    chartView.costOfBorrowingChart.series[1].setData( [ totalBorrowingAtGrad, totalBorrowingAtGrad ] );
  },

  updateMakePlanChart: () => {
    const totalCosts = getFinancialValue( 'total_costs' );
    const totalFunding = getFinancialValue( 'total_funding' );
    const max = Math.max( totalCosts * 1.1, totalFunding * 1.1 );
    const text = 'Cost of attendance<br>' + numberToMoney( { amount: totalCosts, decimalPlaces: 0 } );

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
    const totalDebt = getFinancialValue( 'debt_tenYearTotal' );
    const salary = getFinancialValue( 'salary_annual' );
    const max = Math.max( totalDebt * 1.1, salary * 1.1 );

    const text = 'Median salary of<br>this school\'s graduates<br>' + numberToMoney( { amount: salary, decimalPlaces: 0 } );

    chartView.maxDebtChart.yAxis[0].update( {
      min: 0,
      max: max,
      stackLabels: {
        enabled: true,
        format: 'Projected total debt<br>${total:,.0f}',
        align: 'right'
      },
      plotLines: [ {
        value: salary,
        zIndex: 4,
        label: {
          align: 'center',
          text: text,
          rotation: 0,
          x: 0,
          y: -40
        }
      } ],
      title: false,
      labels: {
        overflow: 'justify'
      }
    } );

    chartView.maxDebtChart.series[0].setData( [ totalDebt ] );
  },

  updateAffordingChart: () => {
    const monthlyExpenses = getExpensesValue( 'total_expenses' );
    const monthlyPayment = getFinancialValue( 'debt_tenYearMonthly' );
    const monthlySalary = getFinancialValue( 'salary_monthly' );

    const max = Math.max( monthlySalary * 1.1, ( monthlyExpenses + monthlyPayment ) * 1.1 );
    const text = 'Monthly Salary<br>' + numberToMoney( { amount: monthlySalary, decimalPlaces: 0 } );

    chartView.affordingChart.yAxis[0].update( {
      max: max,
      plotLines: [ {
        value: monthlySalary,
        zIndex: 4,
        label: {
          align: 'center',
          text: text,
          rotation: 0,
          x: 0,
          y: -30
        }
      } ]
    } );

    chartView.affordingChart.series[0].setData( [ monthlyPayment ] );
    chartView.affordingChart.series[1].setData( [ monthlyExpenses ] );
  },

  updateGradMeterChart: () => {
    const cohort = getSchoolValue( 'cohortRankByControl' );
    let percentile = 0;

    if ( typeof cohort !== 'undefined' ) {
      percentile = cohort.grad_rate.percentile_rank;
    }

    // Percentile works along a 180-degree axis:
    percentile = percentile / 100 * 180;
    chartView.gradMeterChart.series[0].setData( [ percentile ] );
  },

  updateRepaymentMeterChart: () => {
    const cohort = getSchoolValue( 'cohortRankByControl' );
    let percentile = 0;

    if ( typeof cohort !== 'undefined' ) {
      percentile = cohort.repay_3yr.percentile_rank;
    }

    // Percentile works along a 180-degree axis:
    percentile = percentile / 100 * 180;
    chartView.repaymentMeterChart.series[0].setData( [ percentile ] );
  }


};


export {
  chartView
};
