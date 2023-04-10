import { promises } from 'fs';
const { readFile } = promises;
import { dirname } from 'path';
import postcss from 'postcss';
import less from 'less';

const postCSSPlugin = ({ plugins = [], lessOptions = {} }) => ({
  name: 'less-and-postcss',
  setup(build) {
    build.onLoad({ filter: /.\.less$/ }, async (args) => {
      const fileContent = await readFile(args.path, { encoding: 'utf-8' });
      const lessResult = await less.render(fileContent, {
        ...lessOptions,
        filename: args.path,
        rootpath: dirname(args.path),
      });

      const result = await postcss(plugins).process(lessResult.css, {
        from: args.path,
      });

      return {
        contents: result.css,
        loader: 'css',
      };
    });
  },
});

export default postCSSPlugin;
