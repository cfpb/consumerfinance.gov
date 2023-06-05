import { expensesModel } from '../models/expenses-model.js';
import { financialModel } from '../models/financial-model.js';
import { schoolModel } from '../models/school-model.js';
import { stateModel } from '../models/state-model.js';

const urlParameters = {
  iped: 'schoolModel.schoolID',
  oid: 'schoolModel.oid',

  pid: 'stateModel.pid',
  houp: 'stateModel.programHousing',
  typp: 'stateModel.programType',
  prop: 'stateModel.programProgress',
  lenp: 'stateModel.programLength',
  ratp: 'stateModel.programRate',
  depp: 'stateModel.programDependency',
  cobs: 'stateModel.costsQuestion',
  regs: 'stateModel.expensesRegion',
  iqof: 'stateModel.impactOffer',
  iqlo: 'stateModel.impactLoans',
  utm_source: 'stateModel.utmSource',
  utm_medium: 'stateModel.utm_medium',
  utm_campaign: 'stateModel.utm_campaign',
  inpp: 'stateModel.includeParentPlus',

  tuit: 'financialModel.dirCost_tuition',
  hous: 'financialModel.dirCost_housing',
  diro: 'financialModel.dirCost_other',

  book: 'financialModel.indiCost_books',
  indo: 'financialModel.indiCost_other',
  tran: 'financialModel.indiCost_transportation',
  nda: 'financialModel.otherCost_additional',

  pelg: 'financialModel.grant_pell',
  seog: 'financialModel.grant_seog',
  fedg: 'financialModel.grant_otherFederal',
  stag: 'financialModel.grant_state',
  schg: 'financialModel.grant_school',
  tuig: 'financialModel.grant_tuition',
  othg: 'financialModel.grant_other',

  mta: 'financialModel.grant_mta',
  gi: 'financialModel.grant_gibill',
  othm: 'financialModel.grant_servicememberOther',

  stas: 'financialModel.scholarship_state',
  schs: 'financialModel.scholarship_school',
  oths: 'financialModel.scholarship_other',

  wkst: 'financialModel.workStudy_workStudy',

  fell: 'financialModel.fellowAssist_fellowship',
  asst: 'financialModel.fellowAssist_assistantship',

  subl: 'financialModel.fedLoan_directSub',
  unsl: 'financialModel.fedLoan_directUnsub',

  insl: 'financialModel.publicLoan_institutional',
  insr: 'financialModel.rate_institutional',
  insf: 'financialModel.fee_institutional',
  stal: 'financialModel.publicLoan_state',
  star: 'financialModel.rate_state',
  staf: 'financialModel.fee_state',
  npol: 'financialModel.publicLoan_nonprofit',
  npor: 'financialModel.rate_nonprofit',
  npof: 'financialModel.fee_nonprofit',

  pers: 'financialModel.savings_personal',
  fams: 'financialModel.savings_family',
  '529p': 'financialModel.savings_collegeSavings',

  offj: 'financialModel.income_jobOffCampus',
  onj: 'financialModel.income_jobOnCampus',
  eta: 'financialModel.income_employerAssist',
  othf: 'financialModel.income_otherFunding',

  pvl1: 'financialModel.privLoan_privLoan1',
  pvr1: 'financialModel.privloan_privLoanRate1',
  pvf1: 'financialModel.privloan_privLoanFee1',

  plus: 'financialModel.plusLoan_parentPlus',

  cdbt: 'financialModel.existingDebt_amount',

  houx: 'expensesModel.item_housing',
  fdx: 'expensesModel.item_food',
  clhx: 'expensesModel.item_clothing',
  trnx: 'expensesModel.item_transportation',
  hltx: 'expensesModel.item_healthcare',
  entx: 'expensesModel.item_entertainment',
  retx: 'expensesModel.item_retirement',
  taxx: 'expensesModel.item_taxes',
  chcx: 'expensesModel.item_childcare',
  othx: 'expensesModel.item_other',
  dbtx: 'expensesModel.item_currentDebts',
};

const models = {
  expensesModel: expensesModel,
  financialModel: financialModel,
  schoolModel: schoolModel,
  stateModel: stateModel,
};

/**
 * getQueryVariables - Check the url for queryString and interpret it into an object
 * full of key-value pairs.
 * @returns {object} key-value pairs of the queryString
 */
function getQueryVariables() {
  const queryVariables = {};
  const queryStringValues = new Proxy(
    new URLSearchParams(window.location.search),
    {
      get: (queryVariables, prop) => queryVariables.get(prop),
    }
  );

  for (const key in urlParameters) {
    if (queryStringValues[key] !== null) {
      queryVariables[key] = queryStringValues[key].replace(/[^a-z0-9.-]/gi, '');
    }
  }

  return queryVariables;
}

/**
 * _buildUrlQueryString - Retreieve values from the models and transform them into a
 * querystring
 * @returns {string} a formatted query string based on model values
 */
function buildUrlQueryString() {
  let query = '?';

  if (models.stateModel.values.programLevel === 'graduate') {
    urlParameters.plus = 'financialModel.plusLoan_gradPlus';
  }

  /* TODO: Don't bother putting expenses in the URL if they equal the default
     for ( let val in expensesurlParameters ) {
     CHECK IF THE VALUE HAS CHANGED FROM THE DEFAULT
     } */

  for (const key in urlParameters) {
    const variable = urlParameters[key];
    const model = models[variable.split('.')[0]].values;
    const value = model[variable.split('.')[1]];

    if (
      typeof value !== 'undefined' &&
      value !== 0 &&
      value !== null &&
      value !== false &&
      value !== 'not-selected'
    ) {
      if (query.length > 1) query += '&';
      query += key + '=' + value;
    }
  }

  if (query === '?') query = '';

  return query;
}

export { buildUrlQueryString, getQueryVariables, urlParameters };
