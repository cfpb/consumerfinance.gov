/* NOTES:
at-rule-no-unknown -
  This rule enforces only @ rules that appear in the CSS spec,
  however, @plugin appears in Less, so should be ignored.
declaration-block-no-redundant-longhand-properties -
  Turned off.
  TODO: Turn on this rule and work out longhand properties.
declaration-empty-line-before -
  Turned off.
  TODO: Turn on this rule and work out what style we want.
declaration-property-value-no-unknown -
  Turned off for Less per documentation guidance.
function-no-unknown -
  Ignore the 'unit' helper function that comes from Less.
media-feature-range-notation -
  Prefer prefixed values, since Less doesn't support ranges.
no-descending-specificity -
  Turned off, but probably shouldn't be.
  TODO: Turn on this rule and see if issues can be fixed.
number-max-precision -
  TODO: See if long decimal values can be shortened using the unit helper.
rule-empty-line-before -
  Custom setting that differs from stylelint-config-standard.
selector-id-pattern -
  Turned off.
  TODO: Turn on this rule and work out regex for BEM syntax.
selector-class-pattern -
  Turned off.
  TODO: Turn on this rule and work out regex for BEM syntax.
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
    'declaration-block-no-redundant-longhand-properties': null,
    'declaration-empty-line-before': null,
    'declaration-property-value-no-unknown': null,
    'function-no-unknown': [true, { ignoreFunctions: ['unit'] }],
    'media-feature-range-notation': ['prefix'],
    'no-descending-specificity': null,
    'number-max-precision': 10,
    'rule-empty-line-before': [
      'always-multi-line',
      {
        except: 'first-nested',
        ignore: ['after-comment', 'inside-block'],
      },
    ],
    'selector-id-pattern': null,
    'selector-class-pattern': null,
    'less/color-no-invalid-hex': null,
    'less/no-duplicate-variables': null,
  },
};
