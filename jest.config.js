module.exports = {
  verbose: false,
  transform: {
    '^.+\\.jsx?$': 'babel-jest'
  },
  collectCoverage: true,
  collectCoverageFrom: [
    '<rootDir>/cfgov/unprocessed/**/*.js'
  ],
  coveragePathIgnorePatterns: [
    '<rootDir>/node_modules/',
    '<rootDir>/cfgov/unprocessed/apps/.+/node_modules/',
    '<rootDir>/cfgov/unprocessed/apps/.+/webpack-config\.js$',
    '<rootDir>/cfgov/unprocessed/js/routes/'
  ],
  coverageDirectory: '<rootDir>/test/unit_test_coverage'
};
