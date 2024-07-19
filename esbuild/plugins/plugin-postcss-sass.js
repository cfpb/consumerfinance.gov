import { readdirSync } from 'node:fs';
import postcss from 'postcss';
import * as sass from 'sass';
import { pluginProcessIcons } from './postcss-process-icons.js';

const pluginPostCssSass = ({ plugins = [] }) => ({
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

      const result = await postcss([...plugins, pluginProcessIcons]).process(
        sassResult.css,
        {
          from: args.path,
        },
      );

      return {
        contents: result.css,
        loader: 'css',
      };
    });
  },
});

export { pluginPostCssSass };
