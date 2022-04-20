/* NOTES:
at-rule-no-unknown -
  This rule enforces only @ rules that appear in the CSS spec,
  however, @plugin appears in Less, so should be ignored.
declaration-colon-newline-after -
  Turned off because it messes with our format for multi-line declarations.
function-parentheses-space-inside -
  Custom setting that differs from stylelint-config-standard.
rule-empty-line-before -
  Custom setting that differs from stylelint-config-standard.
max-empty-lines -
  Set to 2 since we have existing two line breaks in place. Could be removed.
no-descending-specificity -
  Turned off, but probably shouldn't be.
  TODO: Turn on this rule and see if issues can be fixed.
less/color-no-invalid-hex
less/no-duplicate-variables
  Both of the above settings are turned off till
  https://github.com/ssivanatarajan/stylelint-less/issues/6 is addressed.
*/
module.exports = {
  extends: 'stylelint-config-recommended-less',
  ignoreFiles: [ 'packages/**/node_modules/**/*.less' ],
  customSyntax: 'postcss-less',
  rules: {
    'at-rule-no-unknown': [ true, { ignoreAtRules: 'plugin' } ],
    'declaration-colon-newline-after': null,
    'declaration-empty-line-before': null,
    'function-name-case': [ 'lower', { ignoreFunctions: [ 'filter' ]} ],
    'function-parentheses-space-inside': 'always',
    'rule-empty-line-before': [
      'always-multi-line',
      {
        except: 'first-nested',
        ignore: [ 'after-comment', 'inside-block' ]
      }
    ],
    'indentation': [
      2,
      {
        ignore: 'value'
      }
    ],
    'max-empty-lines': 2,
    'media-feature-parentheses-space-inside': 'always',
    'no-descending-specificity': null,
    'selector-pseudo-class-parentheses-space-inside': 'always',
    'less/color-no-invalid-hex': null,
    'less/no-duplicate-variables': null
  }
};

