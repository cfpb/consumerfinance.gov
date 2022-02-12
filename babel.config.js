// This config is currently only consumed by babel-jest for the unit tests.
module.exports = {
  sourceType: 'unambiguous',
  presets: [ '@babel/preset-env' ],
  plugins: [ '@babel/plugin-transform-runtime' ]
};
