// Run `npx @eslint/config-inspector` to inspect the config.

import globals from 'globals';
import js from '@eslint/js';
import importPlugin from 'eslint-plugin-import';
import jsdoc from 'eslint-plugin-jsdoc';
import jsxA11y from 'eslint-plugin-jsx-a11y';
import reactPlugin from 'eslint-plugin-react';
import pluginCypress from 'eslint-plugin-cypress/flat';
import eslintConfigPrettier from 'eslint-config-prettier';

export default [
  {
    ignores: ['.tox', 'cfgov/static_built', 'collectstatic'],
  },
  js.configs.recommended,
  importPlugin.flatConfigs.recommended,
  jsdoc.configs['flat/recommended'],
  jsxA11y.flatConfigs.recommended,
  reactPlugin.configs.flat.recommended,
  pluginCypress.configs.recommended,
  eslintConfigPrettier,

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
        ...globals.jest,
        ...globals.serviceworker,
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
    // Some plugins are automatically included.
    // plugins: {},
    rules: {
      'import/no-unresolved': [
        2,
        {
          ignore: [
            '@cfpb/cfpb-design-system$',
            '@cfpb/cfpb-design-system/tooltips$',
            '@cfpb/cfpb-design-system/icons/.+.svg$',
          ],
        },
      ],
      'jsdoc/require-hyphen-before-param-description': ['warn', 'always'],
      'no-console': ['warn'],
      'no-use-before-define': ['error', 'nofunc'],
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
    },
  },
];
