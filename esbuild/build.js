import esbuild from 'esbuild';
import { copy } from './copy.js';
import { scripts, jsPaths } from './scripts.js';
import { styles, cssPaths } from './styles.js';

import environment from '../config/environment.js';
const { processed } = environment.paths;

import { runWorkerAndManifest } from '../cfgov/unprocessed/apps/regulations3k/worker_and_manifest.js';

const baseConfig = {
  logLevel: 'info',
  bundle: true,
  minify: true,
  sourcemap: true,
  external: ['*.png', '*.woff2', '*.gif'],
  loader: {
    '.svg': 'text',
  },
  outdir: `${processed}`,
};

const arg = process.argv.slice(2)[0];

(async function () {
  const scriptsConfig = scripts(baseConfig);
  const stylesConfig = styles(baseConfig);
  const mergedConfig = { ...scriptsConfig, ...stylesConfig };
  mergedConfig.entryPoints = jsPaths.concat(cssPaths);

  if (arg === 'watch') {
    const ctx = await esbuild.context(mergedConfig);
    await ctx.watch();
    // Not disposing context here as the user will ctrl+c to end watching.
  } else {
    const ctx = await esbuild.context(mergedConfig);
    await ctx.rebuild();
    await ctx.dispose();
  }

  await copy(baseConfig);

  // Run app-specific scripts
  runWorkerAndManifest();
})();
