import financialView from '../views/financial-view.js';

const getApiValues = {
  values: {},
  constants: function () {
    const urlBase = document.querySelector('main').getAttribute('data-context');
    const url =
      '/' + urlBase + '/understanding-your-financial-aid-offer/api/constants/';
    return fetch(url);
  },

  expenses: function () {
    const urlBase = document.querySelector('main').getAttribute('data-context');
    const url =
      '/' + urlBase + '/understanding-your-financial-aid-offer/api/expenses/';

    return fetch(url);
  },

  fetchSchoolData: function (iped) {
    const urlBase = document.querySelector('main').getAttribute('data-context');
    const url =
      '/' +
      urlBase +
      '/understanding-your-financial-aid-offer/api/school/' +
      iped +
      '/';

    return fetch(url).catch(function (error) {
      financialView.missingData('noSchool');
      return new Error(error);
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

    return fetch(url).catch(function (error) {
      financialView.missingData('noProgram');
      return new Error(error);
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

    return fetch(url);
  },

  schoolData: function (iped, pid) {
    return Promise.all([
      this.fetchSchoolData(iped).then((v) => v.json()),
      this.fetchProgramData(iped, pid).then((v) => v.json()),
      this.fetchNationalData(iped, pid).then((v) => v.json()),
    ]);
  },

  initialData: function () {
    // If there's a [data-warning], display error
    const warning = document
      .querySelector('[data-warning]')
      .getAttribute('data-warning');
    if (warning && !window.Cypress) {
      financialView.missingData(warning);
      return Promise.resolve();
    }
    return Promise.all([
      this.constants().then((v) => v.json()),
      this.expenses().then((v) => v.json()),
    ]);
  },
};

export default getApiValues;
