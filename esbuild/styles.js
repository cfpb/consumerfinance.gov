import esbuild from 'esbuild';
import { readdirSync } from 'fs';
import postCSSPlugin from './plugins/postcss.js';
import autoprefixer from 'autoprefixer';
import { getAll } from './utils.js';

import environment from '../config/environment.js';
const { unprocessed, modules } = environment.paths;

const css = `${unprocessed}/css`;
const apps = `${unprocessed}/apps`;

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
  'filing-instruction-guide',
];

const cssPaths = [
  `${css}/main.less`,
  ...getAll(`${css}/on-demand`, /.less$/),
  ...styledApps.map((app) => `${apps}/${app}/css/main.less`),
];

/**
 *
 * @param baseConfig
 */
function styles(baseConfig) {
  esbuild.build({
    ...baseConfig,
    entryPoints: cssPaths,
    plugins: [
      postCSSPlugin({
        plugins: [autoprefixer],
        lessOptions: {
          math: 'always',
          paths: [
            ...readdirSync(`${modules}/@cfpb`).map(
              (v) => `${modules}/@cfpb/${v}/src`
            ),
            `${modules}/cfpb-chart-builder/src/css`,
            `${modules}`,
          ],
        },
      }),
    ],
  });
}

export { styles };
