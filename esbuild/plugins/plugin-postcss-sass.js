import { readdirSync } from 'node:fs';
import postcss from 'postcss';
import cssnano from 'cssnano';
import autoprefixer from 'autoprefixer';
import * as sass from 'sass';
import { pluginProcessIcons } from './postcss-process-icons.js';

const pluginPostCssSass = () => ({
  name: 'postcss-sass',
  setup(build) {
    build.onLoad({ filter: /.\.scss$/ }, async (args) => {
      const sassResult = await sass.compile(args.path, {
        loadPaths: [
          ...readdirSync('./node_modules/@cfpb').map(
            (v) => `./node_modules/@cfpb/${v}/src`,
          ),
          './node_modules/',
        ],
      });

      const result = await postcss([
        autoprefixer,
        pluginProcessIcons,
        cssnano,
      ]).process(sassResult.css, {
        from: args.path,
      });

      // If the suffix is .component.scss, we're going to assume this
      // will be inlined into a web component, so we'll change the loader
      // from css to text.
      const inlineRegex = /^(?!.*\.component\.scss$).*\.scss$/;

      return {
        contents: result.css,
        loader: inlineRegex.exec(args.path) ? 'css' : 'text',
      };
    });
  },
});

export { pluginPostCssSass };
