import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const pluginProcessIcons = () => {
  const stripQuotes = (str) => str.replace(/['"]+/g, '');

  return {
    postcssPlugin: 'process-icons',
    Declaration: {
      '--cfpb-background-icon-svg': async (decl) => {
        const props = decl.value.split(' ');
        const iconName = stripQuotes(props[0]);
        const iconColor = props.length > 1 ? stripQuotes(props[1]) : '';

        const pathToSVG =
          __dirname +
          '/../../node_modules/@cfpb/cfpb-design-system/src/components/cfpb-icons/icons/' +
          iconName +
          '.svg';
        const rawSVG = await readFileSync(pathToSVG, 'utf8', (err, data) => {
          if (err) console.log(err);

          return data;
        });

        let cleanSVG = rawSVG;
        if (iconColor !== '') {
          cleanSVG = rawSVG.replace(
            /class="cf-icon-svg .+" /,
            `fill="${iconColor}" `,
          );
        }

        decl.prop = 'background-image';
        decl.value = `url('data:image/svg+xml;charset=UTF-8,${cleanSVG}')`;
      },
    },
  };
};
pluginProcessIcons.postcss = true;

export { pluginProcessIcons };
