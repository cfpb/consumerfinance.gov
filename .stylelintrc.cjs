/* NOTES:
at-rule-no-unknown -
  This rule enforces only @ rules that appear in the CSS spec,
  however, @plugin appears in Less, so should be ignored.
rule-empty-line-before -
  Custom setting that differs from stylelint-config-standard.
no-descending-specificity -
  Turned off, but probably shouldn't be.
  TODO: Turn on this rule and see if issues can be fixed.
selector-id-pattern -
  Turned off.
  TODO: Turn on this rule and work out regex for BEM syntax.
selector-class-pattern -
  Turned off.
  TODO: Turn on this rule and work out regex for BEM syntax.
declaration-property-value-no-unknown -
  Turned off for Less per documentation guidance.
declaration-block-no-redundant-longhand-properties -
  Turned off.
  TODO: Turn on this rule and work out longhand properties.
function-no-unknown -
  Ignore the 'unit' helper function that comes from Less.
number-max-precision -
  TODO: See if long decimal values can be shortened using the unit helper.
media-feature-range-notation -
  Prefer prefixed values, since Less doesn't support ranges.
less/color-no-invalid-hex
less/no-duplicate-variables
  Both of the above settings are turned off till
  https://github.com/ssivanatarajan/stylelint-less/issues/6 is addressed.
*/
module.exports = {
  extends: ['stylelint-config-standard'],
  plugins: ['stylelint-less'],
  ignoreFiles: ['packages/**/node_modules/**/*.less'],
  customSyntax: 'postcss-less',
  rules: {
    'at-rule-no-unknown': [true, { ignoreAtRules: 'plugin' }],
    'declaration-empty-line-before': null,
    'declaration-property-value-no-unknown': true,
    'function-name-case': ['lower', { ignoreFunctions: ['filter'] }],
    'rule-empty-line-before': [
      'always-multi-line',
      {
        except: 'first-nested',
        ignore: ['after-comment', 'inside-block'],
      },
    ],
    'no-descending-specificity': null,
    'selector-id-pattern': null,
    'selector-class-pattern': null,
    'declaration-property-value-no-unknown': null,
    'declaration-block-no-redundant-longhand-properties': null,
    'function-no-unknown': [true, { ignoreFunctions: ['unit'] }],
    'number-max-precision': 10,
    'media-feature-range-notation': ['prefix'],
    'less/color-no-invalid-hex': null,
    'less/no-duplicate-variables': null,
  },
};
