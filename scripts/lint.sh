## Run prettier. See ignored path in .prettierignore.
yarn prettier "./**/*.{js,jsx,ts,tsx,md}" --write

## Run JS linting. See ignored path in .eslintignore.
eslint --ignore-pattern node_modules './{cfgov/unprocessed,config,esbuild,scripts,test}/**/*.js' --fix

## Run CSS linting. See ignored path in .stylelintignore.
yarn stylelint './cfgov/unprocessed/**/*.{css,less}' --fix
