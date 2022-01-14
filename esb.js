/* eslint-disable no-sync */
const fs = require( 'fs' );
const esbuild = require( 'esbuild' );
const postCSSPlugin = require( 'esbuild-plugin-postcss2' );
const autoprefixer = require( 'autoprefixer' );

const cfpbModules = './node_modules/@cfpb';

const up = './cfgov/unprocessed';
const css = `${ up }/css`;
const r = `${ up }/js/routes`;
const a = `${ up }/apps`;
const od = `${ r }/on-demand`;

/**
 * @param {string} path The directory with the needed js
 * @param {regex} regex The regex to match against
 * @returns {array} An array of matched files
 */
function getAll( path, regex = /.js$/ ) {
  return fs.readdirSync( path )
    .filter( v => v.match( regex ) )
    .map( v => `${ path }/${ v }` );
}

const jsPaths = [
  // header and footer
  `${ r }/common.js`,

  // js for entire sub-paths
  `${ r }/ask-cfpb/single.js`,
  `${ r }/credit-cards/single.js`,
  `${ r }/es/single.js`,
  // js for specific pages, based on url
  `${ r }/about-us/careers/current-openings/index.js`,
  `${ r }/consumer-tools/debt-collection/index.js`,
  `${ r }/data-research/prepaid-accounts/search-agreements/index.js`,
  `${ r }/owning-a-home/mortgage-estimate/index.js`,
  `${ r }/owning-a-home/index.js`,
  `${ r }/external-site/index.js`,

  // on-demand: components included on a page via Wagtatil
  ...getAll( od ),
  `${ od }/simple-chart/simple-chart.js`,
  `${ od }/youth-employment-programs/buying-a-car/index.js`,
  // apps
  ...getAll( `${ a }/admin/js` ),
  ...getAll( `${ a }/analytics-gtm/js` ),
  `${ a }/ccdb-landing-map/js/index.js`,
  `${ a }/financial-well-being/js/home.js`,
  `${ a }/financial-well-being/js/results.js`,
  `${ a }/find-a-housing-counselor/js/common.js`,
  `${ a }/form-explainer/js/FormExplainer.js`,
  `${ a }/owning-a-home/js/common.js`,
  `${ a }/owning-a-home/js/explore-rates/index.js`,
  `${ a }/owning-a-home/js/mortgage-estimate/index.js`,
  `${ a }/owning-a-home/js/form-explainer/index.js`,
  `${ a }/paying-for-college/js/disclosure-feedback.js`,
  `${ a }/paying-for-college/js/college-costs.js`,
  `${ a }/paying-for-college/js/repay.js`,
  `${ a }/regulations3k/js/index.js`,
  `${ a }/regulations3k/js/permalinks.js`,
  `${ a }/regulations3k/js/recent-notices.js`,
  `${ a }/regulations3k/js/search.js`,
  `${ a }/retirement/js/index.js`,
  `${ a }/rural-or-underserved-tool/js/common.js`,
  `${ a }/teachers-digital-platform/js/index.js`,
  `${ a }/youth-employment-success/js/index.js`
];

const styledApps = [
  'ccdb-landing-map',
  'find-a-housing-counselor',
  'form-explainer',
  'know-before-you-owe',
  'owning-a-home',
  'paying-for-college',
  'prepaid-agreements',
  'regulations3k',
  'retirement',
  'rural-or-underserved-tool',
  'teachers-digital-platform',
  'youth-employment-success'
];

const cssPaths = [
  `${ css }/main.less`,
  `${ css }/header.less`,
  `${ css }/footer.less`,
  ...getAll( `${ css }/on-demand/`, /.less$/ ),
  ...styledApps.map( v => `${ a }/${ v }/css/main.less` )
];

const baseConfig = {
  logLevel: 'info',
  bundle: true,
  minify: true,
  sourcemap: true,
  external: [ '*.png', '*.woff', '*.woff2', '*.gif', '*.svg' ],
  outdir: 'cfgov/static_built/out'
};

// JS
esbuild.build( { ...baseConfig, entryPoints: jsPaths } );

// CSS
esbuild.build( {
  ...baseConfig,
  entryPoints: cssPaths,
  plugins: [ postCSSPlugin.default( {
    plugins: [ autoprefixer ],
    lessOptions: {
      compress: true,
      math: 'always',
      paths: [
        ...fs.readdirSync( cfpbModules ).map( v => `${ cfpbModules }/${ v }/src` ),
        './node_modules/cfpb-chart-builder/src/css'
      ]
    }
  } ) ]
} );

// Run app-specific scripts
require( './cfgov/unprocessed/apps/regulations3k/worker_and_manifest.js' );

