import $ from '../../../../js/modules/util/dollar-sign.js';
import getApiValues from './dispatchers/get-api-values.js';
import verifyOffer from './dispatchers/post-verify.js';
import financialModel from './models/financial-model.js';
import schoolModel from './models/school-model.js';
import expensesModel from './models/expenses-model.js';
import getFinancial from './dispatchers/get-financial-values.js';
import getExpenses from './dispatchers/get-expenses-values.js';
import {
  getUrlOfferExists,
  getUrlValues,
} from './dispatchers/get-url-values.js';
import financialView from './views/financial-view.js';
import expensesView from './views/expenses-view.js';
import metricView from './views/metric-view.js';
import questionView from './views/question-view.js';
import publish from './dispatchers/publish-update.js';
import print from './utils/print-page.js';

const ready = function (callback) {
  if (document.readyState !== 'loading') {
    // Document is already ready, call the callback directly
    callback();
  } else if (document.addEventListener) {
    // All modern browsers to register DOMContentLoaded
    document.addEventListener('DOMContentLoaded', callback);
  } else {
    // Old IE browsers
    document.attachEvent('onreadystatechange', function () {
      if (document.readyState === 'complete') {
        callback();
      }
    });
  }
};

const app = {
  urlValues: {},
  init: function () {
    getApiValues.initialData().then((resp) => {
      if (!resp) return;
      const [constants, expenses] = resp;
      financialModel.init(constants);
      financialView.init();
      if (location.href.indexOf('about-this-tool') === -1) {
        expensesModel.init(expenses);
        expensesView.init();
      }
      if (getUrlOfferExists()) {
        // Check for URL offer data
        this.urlValues = getUrlValues();
        getApiValues
          .schoolData(this.urlValues.collegeID, this.urlValues.programID)
          .then((respArr) => {
            const [schoolData, programData, nationalData] = respArr;
            const data = {};
            Object.assign(data, schoolData, programData, nationalData);
            const schoolValues = schoolModel.init(
              nationalData,
              schoolData,
              programData,
            );
            const $step2 = $('.continue__controls button');

            /* If PID exists, update the financial model and view based
           on program data */
            if (!{}.hasOwnProperty.call(data, 'pidNotFound')) {
              financialModel.updateModelWithProgram(schoolValues);
              financialView.updateViewWithProgram(schoolValues, this.urlValues);
            }

            // Add url values to the financial model
            publish.extendFinancialData(this.urlValues);
            const trueTotalCost = Math.max(
              programData.totalCost,
              this.urlValues.urlTotalCost,
            );
            publish.financialData('totalCost', trueTotalCost);
            financialView.updateViewWithURL(schoolValues, this.urlValues);
            // initialize metric view
            metricView.init();
            financialView.updateView(getFinancial.values());
            questionView.init();

            // Update expenses model bases on region and salary
            const region = schoolValues.BLSAverage.slice(0, 2);
            $('#bls-region-select').val(region).change();
            $step2.removeClass('a-btn--disabled');
            $step2.addClass('a-btn--hide-icon');
            $step2.elements[0].removeAttribute('disabled');
          });
      }
      // set financial caps based on data
      financialView.setCaps(getFinancial.values());
      financialView.updateView(getFinancial.values());
    });
    verifyOffer.init();
    print.init();
  },
};

ready(function () {
  app.init();

  /* The following line allows for functional testing by exposing
     the getFinancial method.
     $( '#financial-offer' ).data( 'getFinancial', getFinancial );
     console.log( $( '#financial-offer' ).data() ); */
  window.getFinancial = getFinancial;
  window.getExpenses = getExpenses;
});
