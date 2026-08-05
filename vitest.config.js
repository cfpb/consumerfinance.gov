import { defineConfig } from 'vitest/config';
import path from 'node:path';

const dirname = import.meta.dirname;

export default defineConfig({
  plugins: [
    {
      name: 'stub-css-imports',
      enforce: 'pre',

      resolveId(id) {
        if (/\.(css|scss)$/.test(id)) {
          return id;
        }
      },

      load(id) {
        if (/\.(css|scss)$/.test(id)) {
          return 'export default {};';
        }
      },
    },
    {
      name: 'stub-assets',
      resolveId(id) {
        if (/\.(svg)$/.test(id)) {
          return id;
        }
      },
      load(id) {
        if (/\.(svg)$/.test(id)) {
          return 'export default "";';
        }
      },
    },
  ],

  test: {
    setupFiles: './test/vitest.setup.js',
    environment: 'jsdom',

    environmentOptions: {
      jsdom: {
        url: 'http://localhost',
      },
    },

    server: {
      deps: {
        inline: ['@cfpb/cfpb-design-system'],
      },
    },

    include: ['**/unit_tests/**/*-spec.js'],

    exclude: ['**/node_modules/**', '**/develop-apps/**'],

    globals: true,

    // Handle the CSS imports that are in JS files:
    css: false,

    coverage: {
      enabled: true,
      provider: 'v8',
      reportsDirectory: 'test/unit_test_coverage',

      include: ['cfgov/unprocessed/**/*.js'],

      exclude: [
        'collectstatic/**',
        'node_modules/**',
        'cfgov/unprocessed/apps/**/node_modules/**',
        'cfgov/unprocessed/apps/**/index.js',
        'cfgov/unprocessed/apps/**/common.js',
        'cfgov/unprocessed/apps/analytics-gtm/js/*.js',
        'cfgov/unprocessed/js/routes/**',
      ],
    },
  },
});
