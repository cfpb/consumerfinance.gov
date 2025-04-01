import { getAll } from './utils.js';
import environment from '../config/environment.js';
const { unprocessed } = environment.paths;

const routes = `${unprocessed}/js/routes`;
const apps = `${unprocessed}/apps`;
const onDemand = `${unprocessed}/js/routes/on-demand`;

const jsPaths = [
  // header and footer
  `${routes}/common.js`,

  // js for entire sub-paths
  `${routes}/credit-cards/single.js`,
  // js for specific pages, based on url
  `${routes}/data-research/prepaid-accounts/search-agreements/index.js`,

  // on-demand: components included on a page via Wagtail
  ...getAll(onDemand),
  `${onDemand}/simple-chart/simple-chart.js`,
  // apps
  ...getAll(`${apps}/admin/js`),
  ...getAll(`${apps}/analytics-gtm/js`),
  `${apps}/agreements/Agreements.jsx`,
  `${apps}/ask-cfpb/js/main.js`,
  `${apps}/careers/js/main.js`,
  `${apps}/ccdb-search/js/main.js`,
  `${apps}/cfpb-chart-builder/js/index.js`,
  `${apps}/financial-well-being/js/home.js`,
  `${apps}/financial-well-being/js/results.js`,
  `${apps}/find-a-housing-counselor/js/common.js`,
  `${apps}/form-explainer/js/index.js`,
  `${apps}/owning-a-home/js/common.js`,
  `${apps}/owning-a-home/js/explore-rates/index.js`,
  `${apps}/paying-for-college/js/disclosures/index.js`,
  `${apps}/paying-for-college/js/college-costs.jsx`,
  `${apps}/prepaid-agreements/js/common.js`,
  `${apps}/regulations3k/js/index.js`,
  `${apps}/regulations3k/js/permalinks.js`,
  `${apps}/regulations3k/js/recent-notices.js`,
  `${apps}/regulations3k/js/search.js`,
  `${apps}/retirement/js/index.js`,
  `${apps}/rural-or-underserved-tool/js/common.js`,
  `${apps}/teachers-digital-platform/js/index.js`,
  `${apps}/filing-instruction-guide/js/fig-init.js`,
  `${apps}/tccp/js/index.js`,
  `${apps}/tccp/js/htmx.js`,
];

/**
 * @param {object} baseConfig - The base esbuild configuration.
 * @returns {object} The modified configuration object.
 */
function scripts(baseConfig) {
  return {
    ...baseConfig,
    entryPoints: jsPaths,
    target: 'es6',
  };
}

export { scripts, jsPaths };
