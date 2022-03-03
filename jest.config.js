module.exports = {
  testEnvironment: 'jsdom',
  verbose: false,
  transform: {
    '^.+\\.jsx?$': 'babel-jest',
    '^.+\\.hbs$': '<rootDir>/test/util/preprocessor-handlebars.js'
  },
  collectCoverage: true,
  collectCoverageFrom: [
    '<rootDir>/cfgov/unprocessed/**/*.js'
  ],
  coveragePathIgnorePatterns: [
    '<rootDir>/collectstatic/',
    '<rootDir>/node_modules/',
    '<rootDir>/cfgov/unprocessed/apps/.+/node_modules/',
    '<rootDir>/cfgov/unprocessed/apps/.+/webpack-config.js$',
    '<rootDir>/cfgov/unprocessed/apps/.+/index.js$',
    '<rootDir>/cfgov/unprocessed/apps/.+/common.js$',
    '<rootDir>/cfgov/unprocessed/apps/analytics-gtm/js/[a-zA-Z-]+.js$',
    '<rootDir>/cfgov/unprocessed/js/routes/'
  ],
  coverageDirectory: '<rootDir>/test/unit_test_coverage',
  moduleNameMapper: {
    '\\.(svg)$': '<rootDir>/test/unit_tests/mocks/fileMock.js'
  },
  testPathIgnorePatterns: [
    '<rootDir>/node_modules/',
    '<rootDir>/develop-apps/'
  ],
  testURL: 'http://localhost',
  transformIgnorePatterns: []
};
