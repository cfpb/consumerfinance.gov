module.exports = {
  parserOptions: {
    sourceType: 'module',
  },
  settings: {
    'import/resolver': {
      node: {
        paths: ['src'],
        extensions: ['.js', '.ts', '.d.ts', '.tsx'],
        moduleDirectory: [
          'node_modules',
        ],
      },
    },
    react: {
      version: 'detect',
    },
  },
  env: {
    browser: true,
    node: true,
    es2021: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:import/errors',
    'plugin:jsdoc/recommended',
    'plugin:jsx-a11y/recommended',
    'plugin:react/recommended',
    'eslint-config-prettier',
  ],
  // Some plugins are automatically included.
  // Run `yarn eslint --print-config foo.js > bar.json` to see included plugins.
  // plugins: [],
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
};
