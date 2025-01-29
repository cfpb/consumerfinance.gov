# Browser support

- We serve JavaScript to any browser that
  [supports fetch](https://caniuse.com/fetch).
  We use [esbuild](https://github.com/evanw/esbuild) to transpile
  and minify our JavaScript.

- We prefix CSS for [every browser in our browserslist](https://github.com/cfpb/consumerfinance.gov/blob/main/package.json#L18).
  We use [autoprefixer](https://github.com/postcss/autoprefixer) to add
  vendor-specific prefixes to rules where necessary.

## Outputting browser support metrics

Within the root directory, run `npx browserslist` to output the set of browser
targets given to `autoprefixer` (CSS) transpiling.

!!! note

    A browserslist string is used in `package.json`.
    See the
    [browserslist docs](https://github.com/browserslist/browserslist#full-list)
    for information on this string and the defaults.

For JavaScript, `esbuild` uses the [`es6`](http://es6-features.org/) target and
our code conditionally includes JavaScript in browsers that
[support fetch](https://caniuse.com/fetch).

!!! note

    JavaScript may still
    be delivered to legacy browsers in the form of our analytics and
    related scripts.

## Current browser support metrics

Twice per year we aim to updated the browser metrics that are fed into our
browserslist config at
[@cfpb/browserslist-config](https://github.com/cfpb/cfpb-analytics/tree/main/packages/browserslist-config).

Per the [best practices published by browserslist](https://github.com/browserslist/browserslist?tab=readme-ov-file#best-practices),
we use a 0.2% cutoff with this config for the browsers
that get fed into our build systems.

However, for what we actively aim to support and test, we use a higher cutoff
of 1%. The current 1% cutoff list is:

```
and_chr 131
chrome 130
chrome 129
chrome 128
chrome 127
chrome 126
chrome 125
edge 127
edge 126
ios_saf 18.0
ios_saf 17.6
ios_saf 17.5
safari 17.6
safari 17.5
```
