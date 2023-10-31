import { promiseRequest } from '../utils/promise-request.js';
import financialView from '../views/financial-view.js';

/**
 * getApi - Make an API request to the endpoint specified with parameters specified
 * @param {string} url - URL of API endpoint
 * @returns {object} Promise
 */
function getApi(url) {
  return new Promise(function (resolve, reject) {
    promiseRequest('GET', url)
      .then(function (resp) {
        resolve(resp);
      })
      .catch(function (error) {
        reject(new Error(error));
      });
  });
}

const getApiValues = {
  values: {},
  constants: function () {
    const urlBase = document.querySelector('main').getAttribute('data-context');
    const url =
      '/' + urlBase + '/understanding-your-financial-aid-offer/api/constants/';
    return getApi(url);
  },

  expenses: function () {
    const urlBase = document.querySelector('main').getAttribute('data-context');
    const url =
      '/' + urlBase + '/understanding-your-financial-aid-offer/api/expenses/';

    return getApi(url);
  },

  fetchSchoolData: function (iped) {
    const urlBase = document.querySelector('main').getAttribute('data-context');
    const url =
      '/' +
      urlBase +
      '/understanding-your-financial-aid-offer/api/school/' +
      iped +
      '/';

    return new Promise(function (resolve ) {
      promiseRequest('GET', url)
        .then(function (resp) {
          resolve(resp);
        })
        .catch(function (error) {
          financialView.missingData('school');
          new Error(error);
        });
    });
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

    const urlBase = document.querySelector('main').getAttribute('data-context');
    const url =
      '/' +
      urlBase +
      '/understanding-your-financial-aid-offer/api/program/' +
      iped +
      '_' +
      pid +
      '/';

    //  $.ajax({
    //   url: url,
    //   dataType: 'json',
    //   success: function (resp) {
    //     return resp;
    //   },
    //   error: function (/* req, status, err */) {
    //     financialView.missingData('program');
    //   },
    // });

    return new Promise(function (resolve ) {
      promiseRequest('GET', url)
        .then(function (resp) {
          resolve(resp);
        })
        .catch(function () {
          financialView.missingData('school');
          // reject(new Error(error));
        });
    });
  },

  fetchNationalData: function (iped, pid) {
    const urlBase = document.querySelector('main').getAttribute('data-context');
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

    return getApi(url);
  },

  schoolData: function (iped, pid) {
    return Promise.all([
      this.fetchSchoolData(iped),
      this.fetchProgramData(iped, pid),
      this.fetchNationalData(iped, pid),
    ]);
  },

  initialData: function () {
    // If there's a [data-warning], display error
    const warning = document
      .querySelector('[data-warning]')
      .getAttribute('data-warning');
    if (warning !== '' && typeof warning !== 'undefined') {
      financialView.missingData(warning);
      const deferred = {};
      deferred.promise = new Promise((resolve, reject) => {
        deferred.resolve = resolve;
        deferred.reject = reject;
      });
      return deferred;
    }
    return Promise.all([this.constants(), this.expenses()]);
  },
};

export default getApiValues;
