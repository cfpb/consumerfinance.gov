// TODO: Remove jquery.
import $ from 'jquery';

import fetch from './dispatchers/get-api-values.js';
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

import('./utils/print-page.js');

const app = {
  init: function () {
    // jquery promise to delay full model creation until ajax resolves
    $.when(fetch.initialData()).done(function (constants, expenses) {
      financialModel.init(constants[0]);
      financialView.init();
      if (location.href.indexOf('about-this-tool') === -1) {
        expensesModel.init(expenses[0]);
        expensesView.init();
      }
      if (getUrlOfferExists()) {
        // Check for URL offer data
        const urlValues = getUrlValues();
        $.when(
          fetch.schoolData(urlValues.collegeID, urlValues.programID)
        ).done(function (schoolData, programData, nationalData) {
          const data = {};
          Object.assign(data, schoolData[0], programData[0], nationalData[0]);
          const schoolValues = schoolModel.init(
            nationalData[0],
            schoolData[0],
            programData[0]
          );

          /* If PID exists, update the financial model and view based
             on program data */
          if (!{}.hasOwnProperty.call(data, 'pidNotFound')) {
            financialModel.updateModelWithProgram(schoolValues);
            financialView.updateViewWithProgram(schoolValues, urlValues);
          }

          // Add url values to the financial model
          publish.extendFinancialData(urlValues);
          if (typeof urlValues.totalCost === 'undefined') {
            publish.financialData('totalCost', null);
          }
          financialView.updateViewWithURL(schoolValues, urlValues);
          // initialize metric view
          metricView.init();
          financialView.updateView(getFinancial.values());
          questionView.init();

          // Update expenses model bases on region and salary
          const region = schoolValues.BLSAverage.substr(0, 2);
          $('#bls-region-select').val(region).change();
        });
      }
      // set financial caps based on data
      financialView.setCaps(getFinancial.values());
      financialView.updateView(getFinancial.values());
    });
    verifyOffer.init();
  },
};

$(document).ready(function () {
  app.init();

  /* The following line allows for functional testing by exposing
     the getFinancial method.
     $( '#financial-offer' ).data( 'getFinancial', getFinancial );
     console.log( $( '#financial-offer' ).data() ); */
  window.getFinancial = getFinancial;
  window.getExpenses = getExpenses;
});
