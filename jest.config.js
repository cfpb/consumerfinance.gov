module.exports = {
  verbose: false,
  transform: {
    '^.+\\.jsx?$': 'babel-jest'
  },
  collectCoverage: true,
  collectCoverageFrom: [
    '!<rootDir>/node_modules/**',
    '!<rootDir>/cfgov/unprocessed/apps/**/node_modules/**',
    '<rootDir>/cfgov/unprocessed/**/*.js'
  ],
  coverageDirectory: '<rootDir>/test/unit_test_coverage'
};
