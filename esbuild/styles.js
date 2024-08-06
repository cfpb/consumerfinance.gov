import { pluginPostCssSass } from './plugins/plugin-postcss-sass.js';
import autoprefixer from 'autoprefixer';
import { getAll } from './utils.js';

import environment from '../config/environment.js';
const { unprocessed } = environment.paths;

const css = `${unprocessed}/css`;
const apps = `${unprocessed}/apps`;

const styledApps = [
  'ask-cfpb',
  'careers',
  'ccdb-search',
  'financial-well-being',
  'find-a-housing-counselor',
  'form-explainer',
  'homepage',
  'know-before-you-owe',
  'owning-a-home',
  'paying-for-college',
  'prepaid-agreements',
  'regulations3k',
  'retirement',
  'rural-or-underserved-tool',
  'teachers-digital-platform',
  'filing-instruction-guide',
  'tccp',
];

const cssPaths = [
  `${css}/main.scss`,
  ...getAll(`${css}/on-demand`, /.scss$/),
  ...styledApps.map((app) => `${apps}/${app}/css/main.scss`),
];

/**
 * @param {object} baseConfig - The base esbuild configuration.
 * @returns {object} The modified configuration object.
 */
function styles(baseConfig) {
  return {
    ...baseConfig,
    entryPoints: cssPaths,
    plugins: [
      pluginPostCssSass({
        plugins: [autoprefixer],
      }),
    ],
  };
}

export { styles, cssPaths };
