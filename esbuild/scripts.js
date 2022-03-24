const esbuild = require( 'esbuild' );
const { getAll } = require( './utils.js' );
const { unprocessed } = require( '../config/environment.js' ).paths;

const routes = `${ unprocessed }/js/routes`;
const apps = `${ unprocessed }/apps`;
const onDemand = `${ unprocessed }/js/routes/on-demand`;

const jsPaths = [
  // header and footer
  `${ routes }/common.js`,

  // js for entire sub-paths
  `${ routes }/ask-cfpb/single.js`,
  `${ routes }/credit-cards/single.js`,
  `${ routes }/es/single.js`,
  `${ routes }/external-site.js`,
  // js for specific pages, based on url
  `${ routes }/about-us/careers/current-openings/index.js`,
  `${ routes }/consumer-tools/debt-collection/index.js`,
  `${ routes }/data-research/prepaid-accounts/search-agreements/index.js`,
  `${ routes }/owning-a-home/mortgage-estimate/index.js`,
  `${ routes }/owning-a-home/index.js`,

  // on-demand: components included on a page via Wagtatil
  ...getAll( onDemand ),
  `${ onDemand }/simple-chart/simple-chart.js`,
  `${ onDemand }/youth-employment-programs/buying-a-car/index.js`,
  // apps
  ...getAll( `${ apps }/admin/js` ),
  ...getAll( `${ apps }/analytics-gtm/js` ),
  `${ apps }/financial-well-being/js/home.js`,
  `${ apps }/financial-well-being/js/results.js`,
  `${ apps }/find-a-housing-counselor/js/common.js`,
  `${ apps }/form-explainer/js/FormExplainer.js`,
  `${ apps }/owning-a-home/js/common.js`,
  `${ apps }/owning-a-home/js/explore-rates/index.js`,
  `${ apps }/owning-a-home/js/mortgage-estimate/index.js`,
  `${ apps }/owning-a-home/js/form-explainer/index.js`,
  `${ apps }/paying-for-college/js/disclosure-feedback.js`,
  `${ apps }/paying-for-college/js/college-costs.js`,
  `${ apps }/paying-for-college/js/repay.js`,
  `${ apps }/regulations3k/js/index.js`,
  `${ apps }/regulations3k/js/permalinks.js`,
  `${ apps }/regulations3k/js/recent-notices.js`,
  `${ apps }/regulations3k/js/search.js`,
  `${ apps }/retirement/js/index.js`,
  `${ apps }/rural-or-underserved-tool/js/common.js`,
  `${ apps }/teachers-digital-platform/js/index.js`
];

module.exports = function( baseConfig ) {
  esbuild.build( { ...baseConfig, entryPoints: jsPaths } );
};
