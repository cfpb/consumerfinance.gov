const esbuild = require( 'esbuild' );
const { readdirSync } = require( 'fs' );
const postCSSPlugin = require( './plugins/postcss.js' );
const autoprefixer = require( 'autoprefixer' );
const { getAll } = require( './utils.js' );

const { unprocessed, modules } = require( '../config/environment.js' ).paths;

const css = `${ unprocessed }/css`;
const apps = `${ unprocessed }/apps`;

const styledApps = [
  'ccdb-search',
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
  'filing-instruction-guide'
];

const cssPaths = [
  `${ css }/main.less`,
  ...getAll( `${ css }/on-demand`, /.less$/ ),
  ...styledApps.map( app => `${ apps }/${ app }/css/main.less` )
];

module.exports = function( baseConfig ) {
  esbuild.build( {
    ...baseConfig,
    entryPoints: cssPaths,
    plugins: [ postCSSPlugin( {
      plugins: [ autoprefixer ],
      lessOptions: {
        math: 'always',
        paths: [
          ...readdirSync( `${ modules }/@cfpb` ).map( v => `${ modules }/@cfpb/${ v }/src` ),
          `${ modules }/cfpb-chart-builder/src/css`,
          `${ modules }`
        ]
      }
    } ) ]
  } );
};

