module.exports = {
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
    '<rootDir>/cfgov/unprocessed/js/routes/'
  ],
  coverageDirectory: '<rootDir>/test/unit_test_coverage',
  moduleNameMapper: {
    '\\.(svg)$': '<rootDir>/test/unit_tests/mocks/fileMock.js'
  }
};
