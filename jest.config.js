module.exports = {
  verbose: false,
  transform: {
    '^.+\\.jsx?$': 'babel-jest',
    '^.+\\.hbs$': '<rootDir>/test/util/preprocessor-handlebars.js'
  },
  collectCoverage: true,
  collectCoverageFrom: [
    '<rootDir>/unprocessed/**/*.js'
  ],
  coveragePathIgnorePatterns: [
    '<rootDir>/collectstatic/',
    '<rootDir>/node_modules/',
    '<rootDir>/unprocessed/apps/.+/node_modules/',
    '<rootDir>/unprocessed/apps/.+/webpack-config.js$',
    '<rootDir>/unprocessed/apps/.+/index.js$',
    '<rootDir>/unprocessed/apps/.+/common.js$',
    '<rootDir>/unprocessed/apps/analytics-gtm/js/[a-zA-Z-]+.js$',
    '<rootDir>/unprocessed/js/routes/'
  ],
  coverageDirectory: '<rootDir>/test/unit_test_coverage',
  moduleNameMapper: {
    '\\.(svg)$': '<rootDir>/test/unit_tests/mocks/fileMock.js'
  },
  testURL: 'http://localhost'
};
