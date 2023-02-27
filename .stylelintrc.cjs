/* NOTES:
at-rule-no-unknown -
  This rule enforces only @ rules that appear in the CSS spec,
  however, @plugin appears in Less, so should be ignored.
rule-empty-line-before -
  Custom setting that differs from stylelint-config-standard.
no-descending-specificity -
  Turned off, but probably shouldn't be.
  TODO: Turn on this rule and see if issues can be fixed.
less/color-no-invalid-hex
less/no-duplicate-variables
  Both of the above settings are turned off till
  https://github.com/ssivanatarajan/stylelint-less/issues/6 is addressed.
*/
module.exports = {
  extends: ['stylelint-config-recommended-less', 'stylelint-config-prettier'],
  ignoreFiles: ['packages/**/node_modules/**/*.less'],
  customSyntax: 'postcss-less',
  rules: {
    'at-rule-no-unknown': [true, { ignoreAtRules: 'plugin' }],
    'declaration-empty-line-before': null,
    'function-name-case': ['lower', { ignoreFunctions: ['filter'] }],
    'rule-empty-line-before': [
      'always-multi-line',
      {
        except: 'first-nested',
        ignore: ['after-comment', 'inside-block'],
      },
    ],
    'no-descending-specificity': null,
    'less/color-no-invalid-hex': null,
    'less/no-duplicate-variables': null,
  },
};
