import globals from 'globals';
import eslintJs from '@eslint/js';
import eslintPluginImport from 'eslint-plugin-import';
import jsdoc from 'eslint-plugin-jsdoc';
import eslintPluginJsxA11y from 'eslint-plugin-jsx-a11y';
import eslintPluginReact from 'eslint-plugin-react';
//import eslintPluginCypress from 'eslint-plugin-cypress';
import eslintPrettierConfig from 'eslint-config-prettier';

export default [
  eslintJs.configs.recommended,
  //eslintPluginImport.flatConfigs.recommended,
  //eslintPluginJsdoc.configs['flat/recommended'],
  //eslintPluginJsxA11y.flatConfigs.recommended,
  //eslintPluginReact.configs.flat.recommended,
  //eslintPluginCypress.configs.recommended,
  //eslintPrettierConfig,

  {
    languageOptions: {
      ecmaVersion: 2023,
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    settings: {
      'import/resolver': {
        node: {
          paths: ['src'],
          extensions: ['.js', '.ts', '.d.ts', '.tsx'],
          moduleDirectory: ['node_modules'],
        },
      },
      react: {
        version: 'detect',
      },
    },
    /*
    extends: [
      'eslint:recommended',
      'plugin:import/errors',
      'plugin:jsdoc/recommended',
      'plugin:jsx-a11y/recommended',
      'plugin:react/recommended',
      'eslint-config-prettier',
    ],*/
    // Some plugins are automatically included.
    // Run `yarn eslint --print-config foo.js > bar.json` to see included plugins.
    plugins: { jsdoc },
    rules: {
      'jsdoc/require-hyphen-before-param-description': ['warn', 'always'],
      'no-console': ['warn'],
      'no-use-before-define': ['error'],
      'no-unused-vars': [
        'error',
        {
          vars: 'all',
          args: 'after-used',
          ignoreRestSiblings: false,
        },
      ],
      'no-var': ['error'],
      'prefer-const': ['error'],
      radix: ['error'],
      // TODO: remove this and fix definition order.
      'no-use-before-define': 0,
    },
  },
];
