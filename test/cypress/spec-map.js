import path from 'path';
import { fileURLToPath } from 'url';
import { readFileSync, writeFileSync } from 'node:fs';
import * as readline from 'node:readline';
import { stdin as input, stdout as output } from 'node:process';

const __filename = fileURLToPath(import.meta.url);
const rootdir = path.join(path.dirname(__filename), '../..');

const FULL_SUITE = "'test/cypress/integration/**/*.cy.{js,jsx,ts,tsx}'";

const rl = readline.createInterface({ input, output, terminal: false });

const candidates = [];

const directories = [
  [
    [
      'cfgov/unprocessed/apps/filing-instruction-guide',
      'cfgov/filing_instruction_guide',
      'cfgov/unprocessed/js/organisms/SecondaryNav.js',
      'cfgov/unprocessed/css/organisms/secondary-nav.scss',
      'cfgov/v1/jinja2/v1/includes/organisms/secondary-nav-fig.html',
    ],
    'compliance/small-business-lending',
  ],
  [[/cfgov\/v1\/.*\.py/], 'admin'],
  [
    ['cfgov/unprocessed/apps/ask-cfpb', 'cfgov/ask_cfpb'],
    'consumer-tools/ask-cfpb',
  ],
  [
    [
      'cfgov/unprocessed/apps/retirement',
      'cfgov/retirement_api',
      'cfgov/unprocessed/js/modules/util/format.js',
    ],
    'consumer-tools/before-you-claim',
  ],
  [
    [
      'cfgov/unprocessed/apps/tccp',
      'cfgov/tccp',
      'cfgov/unprocessed/js/modules/util/web-storage-proxy',
    ],
    'consumer-tools/credit-cards',
  ],
  [
    ['cfgov/unprocessed/apps/financial-well-being', 'cfgov/wellbeing'],
    'consumer-tools/financial-well-being',
  ],
  [
    [
      'cfgov/unprocessed/apps/find-a-housing-counselor',
      'cfgov/housing_counselor',
    ],
    'consumer-tools/find-a-housing-counselor',
  ],
  [
    ['cfgov/unprocessed/apps/ask-cfpb', 'cfgov/ask_cfpb'],
    'consumer-tools/obtener-respuestas',
  ],
  [
    [
      'cfgov/unprocessed/apps/owning-a-home',
      'cfgov/jinja2/owning-a-home',
      'cfgov/unprocessed/js/modules/util/format.js',
    ],
    'consumer-tools/owning-a-home',
  ],
  [
    [
      'cfgov/unprocessed/apps/rural-or-underserved-tool',
      'cfgov/jinja2/rural-or-underserved',
    ],
    'consumer-tools/rural-or-underserved-tool',
  ],
  [
    [
      'cfgov/unprocessed/apps/teachers-digital-platform',
      'cfgov/teachers_digital_platform',
    ],
    'consumer-tools/tdp-activity-search',
  ],
  [
    [
      'cfgov/unprocessed/js/routes/on-demand/chart.js',
      'cfgov/unprocessed/css/on-demand/chart.scss',
      'cfgov/v1/jinja2/v1/includes/organisms/chart.html',
      /cfgov\/v1\/.*\.py/,
    ],
    'components/cct-charts',
  ],
  [
    [
      'cfgov/unprocessed/js/routes/on-demand/email-signup.js',
      'cfgov/v1/jinja2/v1/includes/blocks/email-signup.html',
      /cfgov\/v1\/.*\.py/,
    ],
    'components/email-signup',
  ],
  [
    [
      'cfgov/unprocessed/js/routes/on-demand/filterable-list-controls.js',
      'cfgov/unprocessed/js/organisms/FilterableListControls.js',
      'cfgov/unprocessed/js/modules/util/FormModel.js',
      'cfgov/unprocessed/css/organisms/filterable-list-controls.scss',
      'cfgov/v1/jinja2/v1/includes/organisms/filterable-list-controls.html',
      'cfgov/v1/jinja2/v1/includes/organisms/filterable-list-results.html',
      /cfgov\/v1\/.*\.py/,
    ],
    'components/filterable-lists',
  ],
  [
    [
      'cfgov/unprocessed/js/organisms/Footer.js',
      'cfgov/unprocessed/js/modules/footer-button.js',
      'cfgov/unprocessed/css/organisms/footer.scss',
      'cfgov/v1/jinja2/v1/includes/organisms/footer.html',
      /cfgov\/v1\/.*\.py/,
    ],
    'components/footer',
  ],
  [
    [
      'cfgov/unprocessed/js/organisms/header.js',
      'cfgov/unprocessed/js/organisms/MegaMenu.js',
      'cfgov/unprocessed/js/organisms/MegaMenuDesktop.js',
      'cfgov/unprocessed/js/organisms/MegaMenuMobile.js',
      'cfgov/unprocessed/js/molecules/GlobalSearch.js',
      'cfgov/unprocessed/css/organisms/header.scss',
      'cfgov/unprocessed/css/organisms/mega-menu.scss',
      'cfgov/unprocessed/css/molecules/global-eyebrow.scss',
      'cfgov/unprocessed/css/molecules/global-header-cta.scss',
      'cfgov/unprocessed/css/molecules/global-search.scss',
      'cfgov/v1/jinja2/v1/includes/organisms/header.html',
      'cfgov/mega_menu/jinja2/mega_menu',
      'cfgov/v1/jinja2/v1/includes/molecules/global-eyebrow.html',
      'cfgov/v1/jinja2/v1/includes/molecules/global-search.html',
      'cfgov/v1/jinja2/v1/includes/molecules/global-header-cta.html',
      /cfgov\/v1\/.*\.py/,
    ],
    'components/header',
  ],
  [['cfgov/v1/jinja2/v1/layouts/base.html'], 'components/meta'],
  [
    [
      'cfgov/unprocessed/css/organisms/filterable-list-controls.scss',
      'cfgov/unprocessed/js/organisms/FilterableListControls.js',
      'cfgov/v1/jinja2/v1/includes/organisms/filterable-list-controls.html',
      /cfgov\/v1\/.*\.py/,
    ],
    'components/multiselect',
  ],
  [
    [
      'cfgov/v1/jinja2/v1/includes/molecules/pagination.html',
      /cfgov\/v1\/.*\.py/,
    ],
    'components/pagination',
  ],
  [['cfgov/agreements'], 'data-research/credit-card-agreements-search'],
  [
    ['cfgov/unprocessed/apps/prepaid-agreements', 'cfgov/prepaid_agreements'],
    'data-research/prepaid-agreements-search',
  ],
  [
    [
      'cfgov/unprocessed/js/routes/on-demand/mortgage-performance-trends.js',
      'cfgov/unprocessed/css/on-demand/mortgage-performance-trends.scss',
      'cfgov/unprocessed/css/on-demand/chart.scss',
      'cfgov/unprocessed/js/organisms/MortgagePerformanceTrends',
      'cfgov/v1/jinja2/v1/includes/organisms/mortgage-chart.html',
      'cfgov/v1/jinja2/v1/includes/organisms/mortgage-map.html',
      /cfgov\/v1\/.*\.py/,
      'cfgov/data_research/models.py',
    ],
    'data-research/mortgage-performance-trends',
  ],
  [
    [
      'cfgov/unprocessed/apps/paying-for-college',
      'cfgov/unprocessed/js/organisms/SecondaryNav.js',
      'cfgov/unprocessed/css/organisms/secondary-nav.scss',
      'cfgov/paying_for_college',
    ],
    'paying-for-college/disclosures',
  ],
  [
    [
      'cfgov/unprocessed/apps/paying-for-college',
      'cfgov/unprocessed/js/organisms/SecondaryNav.js',
      'cfgov/unprocessed/css/organisms/secondary-nav.scss',
      'cfgov/paying_for_college',
    ],
    'paying-for-college/your-financial-path-to-graduation',
  ],
  [
    ['cfgov/unprocessed/apps/regulations3k', 'cfgov/regulations3k'],
    'rules-policy',
  ],
  [
    [
      'test/cypress/spec-map.js',
      'requirements/',
      /^package.json/,
      /cfgov\/core\/.*\.py/,
      'cfgov/v1/jinja2/v1/layouts/base.html',
    ],
    'all',
  ],
];

rl.on('line', (file) => {
  console.log('File changed:', file);
  for (const [dList, candidate] of directories) {
    for (const directory of dList) {
      if (file.match(directory)) {
        candidates.push(candidate);
        break;
      }
    }
    if (file.match('test/cypress/integration/' + candidate)) {
      candidates.push(candidate);
    }
  }
});

rl.on('close', () => {
  const deduped = new Set(candidates);
  if (deduped.has('all')) {
    console.log('\nChange requires full Cypress suite.');
    rewriteConfig(FULL_SUITE);
  } else {
    console.log(
      '\nChange requires running Cypress tests in the following directories:\n' +
        [...deduped].join('\n'),
    );
    rewriteConfig(
      JSON.stringify(
        [...deduped].map((v) => {
          return `test/cypress/integration/${v}/*.cy.{js,jsx,ts,tsx}`;
        }),
      ),
    );
  }
});

/**
 * @param {string} specPattern - The spec pattern(s) to match
 */
function rewriteConfig(specPattern) {
  if (specPattern === '[]') specPattern = "'test/cypress/dummy.cy.js'";
  const tmpl = readFileSync(path.join(rootdir, 'cypress.template.mjs'), {
    encoding: 'utf8',
  });
  const config = tmpl.replace(FULL_SUITE, specPattern);
  writeFileSync(path.join(rootdir, 'cypress.config.mjs'), config);
}
