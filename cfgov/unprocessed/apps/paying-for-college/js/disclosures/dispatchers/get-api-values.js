// TODO: Remove jquery.
import $ from 'jquery';

import financialView from '../views/financial-view.js';

const getApiValues = {
  values: {},

  constants: function () {
    const urlBase = document
      .querySelector('main')
      .getAttribute('data-context');
    const url =
      '/' + urlBase + '/understanding-your-financial-aid-offer/api/constants/';
    const constantsRequest = $.ajax({
      url: url,
      dataType: 'json',
      success: function (resp) {
        return resp;
      },
      // TODO: the user should be notified of errors
      // eslint-disable-next line no-unused-vars
      error: function (req, status, err) {
        console.log('API: constants', status, err);
      },
    });
    return constantsRequest;
  },

  expenses: function () {
    const urlBase = document
      .querySelector('main')
      .getAttribute('data-context');
    const url =
      '/' + urlBase + '/understanding-your-financial-aid-offer/api/expenses/';
    const expensesRequest = $.ajax({
      url: url,
      dataType: 'json',
      success: function (resp) {
        return resp;
      },
      // TODO: the user should be notified of errors
      error: function (req, status, err) {
        console.log('API: expenses', status, err);
      },
    });
    return expensesRequest;
  },

  fetchSchoolData: function (iped) {
    const urlBase = document
      .querySelector('main')
      .getAttribute('data-context');
    const url =
      '/' +
      urlBase +
      '/understanding-your-financial-aid-offer/api/school/' +
      iped +
      '/';
    const schoolDataRequest = $.ajax({
      url: url,
      dataType: 'json',
      success: function (resp) {
        return resp;
      },
      error: function (/* req, status, err */) {
        financialView.missingData('school');
      },
    });

    return schoolDataRequest;
  },

  fetchProgramData: function (iped, pid) {
    if (!pid) {
      return [
        {
          pidNotFound:
            'An invalid program ID was passed to the ' +
            'fetchProgramData request.',
        },
      ];
    }

    const urlBase = document
      .querySelector('main')
      .getAttribute('data-context');
    const url =
      '/' +
      urlBase +
      '/understanding-your-financial-aid-offer/api/program/' +
      iped +
      '_' +
      pid +
      '/';
    const programDataRequest = $.ajax({
      url: url,
      dataType: 'json',
      success: function (resp) {
        return resp;
      },
      error: function (/* req, status, err */) {
        financialView.missingData('program');
      },
    });

    return programDataRequest;
  },

  fetchNationalData: function (iped, pid) {
    const urlBase = document
      .querySelector('main')
      .getAttribute('data-context');
    let url =
      '/' +
      urlBase +
      '/understanding-your-financial-aid-offer/api/national-stats/' +
      iped;

    if (typeof pid === 'undefined') {
      url += '/';
    } else {
      url += '_' + pid + '/';
    }

    const nationalDataRequest = $.ajax({
      url: url,
      dataType: 'json',
      success: function (resp) {
        return resp;
      },
      // TODO: the user should be notified of errors
      error: function (req, status, err) {
        console.log('API: fetchNationalData', status, err);
      },
    });

    return nationalDataRequest;
  },

  schoolData: function (iped, pid) {
    return $.when(
      this.fetchSchoolData(iped),
      this.fetchProgramData(iped, pid),
      this.fetchNationalData(iped, pid)
    );
  },

  initialData: function () {
    // If there's a [data-warning], display error
    const warning = document
      .querySelector('[data-warning]')
      .getAttribute('data-warning');
    if (warning !== '' && typeof warning !== 'undefined') {
      financialView.missingData(warning);
      return $.Deferred;
    }
    return $.when(this.constants(), this.expenses());
  },
};

export default getApiValues;
