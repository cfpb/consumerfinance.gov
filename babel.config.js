// This config is currently only consumed by babel-jest for the unit tests.
module.exports = {
  presets: [ '@babel/preset-env' ],
  plugins: [ '@babel/plugin-transform-runtime' ]
};
