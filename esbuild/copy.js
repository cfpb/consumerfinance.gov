import * as fs from 'fs';
const { mkdir, copyFile } = fs.promises;
import { dirname, resolve } from 'path';
import { getFiles, copyAll } from './utils.js';
import environment from '../config/environment.js';
const { unprocessed, modules } = environment.paths;

/**
 * @param {object} baseConfig - The base esbuild configuration.
 */
async function copy(baseConfig) {
  const resolvedBase = resolve(unprocessed);
  const files = await getFiles(resolvedBase);

  const staticFiles = files.filter(
    (v) => !v.match(/\/\.[-.\w]*$|\.js$|\.less$|\.css$/i),
  );

  const inDirs = [...new Set(staticFiles.map((v) => dirname(v)))];

  const outDirs = [
    ...inDirs.map((v) => v.replace(resolvedBase, baseConfig.outdir)),
    // Create specific icon directory
    `${baseConfig.outdir}/icons`,
  ];

  // Make output directories
  await Promise.all(outDirs.map((d) => mkdir(d, { recursive: true })));

  // Copy files to output directories
  staticFiles.forEach((f) =>
    copyFile(f, f.replace(resolvedBase, baseConfig.outdir)),
  );

  // Handle files that live at the root of the site
  copyAll(`${unprocessed}/root`, baseConfig.outdir);

  // Handle icons
  copyAll(
    `${modules}/@cfpb/cfpb-icons/src/icons`,
    `${baseConfig.outdir}/icons`,
  );
}

export { copy };
