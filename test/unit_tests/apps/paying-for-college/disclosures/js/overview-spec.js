import financialView from '../../../../../../cfgov/unprocessed/apps/paying-for-college/js/disclosures/views/financial-view.js';
import financialModel from '../../../../../../cfgov/unprocessed/apps/paying-for-college/js/disclosures/models/financial-model.js';
import expensesModel from '../../../../../../cfgov/unprocessed/apps/paying-for-college/js/disclosures/models/expenses-model.js';
import schoolModel from '../../../../../../cfgov/unprocessed/apps/paying-for-college/js/disclosures/models/school-model.js';
import { getUrlValues } from '../../../../../../cfgov/unprocessed/apps/paying-for-college/js/disclosures/dispatchers/get-url-values.js';
import publishUpdate from '../../../../../../cfgov/unprocessed/apps/paying-for-college/js/disclosures/dispatchers/publish-update.js';
import HTML_SNIPPET from '../fixtures/overview.js';
import {
  constants,
  expenses,
  national,
  school,
  program,
} from '../fixtures/index.js';

describe('Disclosures', () => {
  beforeEach(() => {
    document.body.innerHTML = HTML_SNIPPET;
    delete global.location;
    global.location = {
      search:
        '?iped=133465&pid=5287&oid=ABCDEABCDEABCDEABCDEABCDEABCDEABCDEABCDE&totl=45000&tuit=38976&hous=3000&book=650&tran=500&othr=500&pelg=1500&schg=2000&stag=2000&othg=100&ta=3000&mta=3000&gib=3000&wkst=3000&parl=14000&perl=3000&subl=15000&unsl=2000&ppl=1000&gpl=1000&prvl=3000&prvi=4.55&prvf=1.01&insl=3000&insi=4.55&inst=8&leng=30%27;#info-right',
    };
  });

  it('renders data into the financial model', () => {
    financialModel.init(constants);
    expect(financialModel.values).toBeTruthy();
  });

  it('initializes the expenses model', () => {
    expensesModel.init(expenses);
    expect(expensesModel.values.stored).toBeTruthy();
  });

  it('extracts url values into an expected object', () => {
    expect(getUrlValues().tuitionFees).toBe(38976);
  });

  it('initializes the school model', () => {
    schoolModel.init(national, school, program);
    expect(schoolModel.values.medianSalary).toBe(33400);
  });

  it('extends the financial model with url values', () => {
    publishUpdate.extendFinancialData(getUrlValues());
    expect(financialModel.values.urlTotalCost).toBe(45000);
    expect(financialModel.values.costOfAttendance).toBe(43626);
  });

  it('updates financial data on input change', () => {
    const tuitionInput = document.getElementById('costs__tuition');
    tuitionInput.value = 40000;
    financialView.inputHandler('costs__tuition');
    expect(financialModel.values.costOfAttendance).toBe(44650);
  });
});
