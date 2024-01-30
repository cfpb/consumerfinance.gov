import { promises, readdirSync } from 'fs';
const { readdir, copyFile } = promises;
import { resolve } from 'path';

/**
 * @param {string} path - The directory with the needed js
 * @param {regex} regex - The regex to match against
 * @returns {Array} An array of matched files
 */
function getAll(path, regex = /.js$/) {
  return readdirSync(path)
    .filter((v) => v.match(regex))
    .map((v) => `${path}/${v}`);
}

// Files that should not be copied and directories that should not be walked
const blocklist = [
  'node_modules',
  'npm-packages-offline-cache',
  '.yarnrc',
  'yarn.lock',
  'package.json',
  '.gitkeep',
  'root',
];

/**
 * @param {string} dir - Current directory to walk.
 * @returns {Array} The list of filtered files from the `dir` directory.
 */
async function getFiles(dir) {
  const dirents = await readdir(dir, { withFileTypes: true });
  const files = await Promise.all(
    dirents.map((dirent) => {
      if (blocklist.indexOf(dirent.name) > -1) return '';
      const res = resolve(dir, dirent.name);
      return dirent.isDirectory() ? getFiles(res) : res;
    }),
  );
  return files.flat().filter((v) => v);
}

/**
 * @param {string} from - Directory to copy files from
 * @param {string} to - Directory to copy files to
 * @returns {Array} Array of promises for each copied file
 */
async function copyAll(from, to) {
  const rFrom = resolve(from);
  const rTo = resolve(to);
  const files = await getFiles(rFrom);
  return files.map((f) => copyFile(f, f.replace(rFrom, rTo)));
}

export { getAll, getFiles, copyAll };
