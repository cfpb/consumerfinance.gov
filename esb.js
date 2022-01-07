/* eslint-disable no-sync */
const fs = require( 'fs' );
const up = './cfgov/unprocessed';
const r = `${ up }/js/routes`;
const a = `${ up }/apps`;
const od = `${ r }/on-demand`;

/**
 * @param {string} path The directory with the needed js
 * @returns {array} An array of matched js files
 */
function getAllJs( path ) {
  return fs.readdirSync( path )
    .filter( v => v.match( /.js$/ ) )
    .map( v => `${ path }/${ v }` );
}

const paths = [
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
  ...getAllJs( od ),
  `${ od }/simple-chart/simple-chart.js`,
  `${ od }/youth-employment-programs/buying-a-car/index.js`,
  // apps
  ...getAllJs( `${ a }/admin/js` ),
  ...getAllJs( `${ a }/analytics-gtm/js` ),
  `${ a }/ccdb-landing-map/js/index.js`,
  `${ a }/financial-well-being/js/home.js`,
  `${ a }/financial-well-being/js/results.js`,
  `${ a }/find-a-housing-counselor/js/common.js`,
  `${ a }/form-explainer/js/FormExplainer.js`,
  `${ a }/owning-a-home/js/common.js`,
  `${ a }/owning-a-home/js/explore-rates/index.js`,
  `${ a }/owning-a-home/js/mortgage-estimate/index.js`,
  `${ a }/owning-a-home/js/form-explainer/index.js`,
  `${ a }/retirement/js/index.js`
];

/* eslint-disable-next-line */
require( 'esbuild' ).buildSync( {
  entryPoints: paths,
  logLevel: 'info',
  bundle: true,
  minify: true,
  loader: {
    '.svg': 'text'
  },
  outdir: 'cfgov/static_built/out'
} );
