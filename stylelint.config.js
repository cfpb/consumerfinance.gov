/* NOTES:
at-rule-no-unknown -
  Ignore to allow at rules from Sass.
color-function-notation -
  Set to 'legacy' to support older browsers in our browserslist (for now).
declaration-block-no-redundant-longhand-properties -
  Turned off.
  TODO: Turn on this rule and work out longhand properties.
declaration-empty-line-before -
  Turned off.
  TODO: Turn on this rule and work out what style we want.
media-feature-range-notation -
  Prefer prefixed values, traditionally used since Less doesn't support ranges.
  TODO: Turn on this rule and migrate to newer style.
no-descending-specificity -
  Turned off, but probably shouldn't be.
  TODO: Turn on this rule and see if issues can be fixed.
number-max-precision -
  TODO: See if long decimal values can be shortened.
rule-empty-line-before -
  Custom setting that differs from stylelint-config-standard.
selector-id-pattern -
  Turned off.
  TODO: Turn on this rule and work out regex for BEM syntax.
selector-class-pattern -
  getBEM style syntax check for classes.
scss/operator-no-newline-after -
  Turned off. Prettier(?) wraps long lines, so sometimes the + operator ends up
  at the end of the line.
scss/comment-no-empty -
  Turned off. Allow empty comments, for visual formatting purposes.
*/
export default {
  extends: ['stylelint-config-standard-scss'],
  ignoreFiles: ['packages/**/node_modules/**/*.scss'],
  rules: {
    'at-rule-no-unknown': null,
    'color-function-notation': ['legacy'],
    'declaration-block-no-redundant-longhand-properties': null,
    'declaration-empty-line-before': null,
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
    'selector-class-pattern': [
      '^[a-z]([a-z0-9-]+)?(__([a-z0-9]+-?)+)?(--([a-z0-9]+-?)+){0,2}$',
      { resolveNestedSelectors: true },
    ],
    'scss/operator-no-newline-after': null,
    'scss/comment-no-empty': null,
  },
};
