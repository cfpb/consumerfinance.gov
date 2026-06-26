import { readFileSync, readdirSync } from 'node:fs';
import postcss from 'postcss';
import cssnano from 'cssnano';
import autoprefixer from 'autoprefixer';
import * as sass from 'sass';

const loadPaths = [
  ...readdirSync('./node_modules/@cfpb').map(
    (v) => `./node_modules/@cfpb/${v}/src`,
  ),
  './node_modules/',
];

/**
 * Convert SCSS to CSS.
 * @param {string} filePath - The absolute file system path.
 */
async function compileSass(filePath) {
  const result = sass.compile(filePath, { loadPaths });
  return result.css;
}

// … Process CSS.
const postCssProcessor = postcss([autoprefixer, cssnano]);

/**
 * @param {string} source - Raw CSS, either from SCSS or from disk.
 * @param {string} from - The absolute file system path.
 */
async function processCss(source, from) {
  return postCssProcessor.process(source, { from });
}

// … The actual plugin definition.
const pluginPostCssSass = () => ({
  name: 'postcss-sass',

  setup(build) {
    build.onLoad({ filter: /\.(css|scss)$/ }, async (args) => {
      // Web Component style files may be styles.component.scss or styles.component.css,
      const isComponent = /\.component\.(css|scss)$/.test(args.path);

      // CSS may come in via .css or .scss files.
      const isScss = args.path.endsWith('.scss');

      let source;

      if (isScss) {
        source = await compileSass(args.path);
      } else {
        source = readFileSync(args.path, 'utf8');
      }

      const result = await processCss(source, args.path);

      return {
        contents: result.css,
        loader: isComponent ? 'text' : 'css',
      };
    });
  },
});

export { pluginPostCssSass };
