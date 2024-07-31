import React, { useState } from 'react';
import { SecondaryNav } from '../../../js/organisms/SecondaryNav.js';
import { appView } from './college-costs/views/app-view.js';
import { chartView } from './college-costs/views/chart-view.js';
import { constantsModel } from './college-costs/models/constants-model.js';
import { expensesModel } from './college-costs/models/expenses-model.js';
import { expensesView } from './college-costs/views/expenses-view.js';
import { financialModel } from './college-costs/models/financial-model.js';
import { financialView } from './college-costs/views/financial-view.js';
import { getQueryVariables } from './college-costs/util/url-parameter-utils.js';
import { navigationView } from './college-costs/views/navigation-view.js';
import { schoolView } from './college-costs/views/school-view.js';
import { updateModelsFromQueryString } from './college-costs/dispatchers/update-models.js';
import { toolTipTracking } from './college-costs/util/analytics.js';

import { createRoot } from 'react-dom/client';
import { Tooltip } from 'react-tooltip';
import Stepper from './Stepper.jsx';

/**
 * Initialize the app
 */
function init() {
  const body = document.querySelector('body');
  const query = getQueryVariables();

  expensesModel.init(body);
  constantsModel.init();
  expensesView.init();
  financialModel.init();
  schoolView.init(body);
  navigationView.init(body, query.iped, getAndSetCallback);
  financialView.init();
  chartView.init(body);
  appView.init();
  SecondaryNav.init();

  financialView.updateFinancialItems();
  appView.updateUI();
  updateModelsFromQueryString(query);
  toolTipTracking();
}

window.addEventListener('load', init);

// Set up Stepper

// const headings = Array.from(
//       document.querySelectorAll('.o-secondary-nav__link')
//     ).map( (obj) => obj.text.trim() );

// const stepMap = Object.fromEntries(
//     Array.from(
//       document.querySelectorAll( '.o-secondary-nav__link' ) )
//       .map( (obj, i) => [ obj.dataset.nav_section , i + 1 ] ) );

const headings = [
  'Calculating school costs',
  'Estimating your debt',
  'Customizing your estimate ',
  'Affording your loans',
  'Comparing your school',
  'Reviewing your plan',
];

const stepMap = {
  'school-info': 1,
  'school-costs': 1,
  'estimate-debt': 2,
  'debt-at-grad': 2,
  'customize-estimate': 3,
  'debt-guideline': 3,
  'cost-of-borrowing': 4,
  'affording-payments': 4,
  'compare-school': 5,
  'review-plan': 6,
};

let getAndSetCallback;

function Wrapper() {
  const [step, setStep] = useState(1);

  function getAndSetStep(activeName) {
    return setStep(stepMap[activeName]);
  }

  getAndSetCallback = getAndSetStep;

  return step ? (
    <Stepper steps={headings.length} step={step} headings={headings} />
  ) : null;
}

const root = createRoot(document.getElementById('react-stepper'));
root.render(<Wrapper />);

const tooltipRoot = createRoot(document.getElementById('react-tooltip'));
tooltipRoot.render(
  <Tooltip
    id="a-tooltip"
    border="1px solid var(--gray-40)"
    opacity="1"
    clickable={true}
    globalCloseEvents={{ escape: true }}
  />,
);
