<!-- Enter an explanation of what the pull request does and why. -->


---

<!-- Feel free to delete any sections that are not applicable to this PR. -->


## Additions

-


## Removals

-


## Changes

-


## How to test this PR

1.


## Screenshots


## Notes and todos

-


## Checklist

<!-- Feel free to delete any checkboxes that are not applicable to this PR. -->

- [ ] PR has an informative and human-readable title
  - PR titles are used to generate the change log in [releases](../../releases); good ones make that easier to scan.
  - Consider prefixing, e.g., "Mega Menu: fix layout bug", or "Docs: Update Docker installation instructions".
- [ ] Changes are limited to a single goal (no scope creep)
- [ ] Code follows the standards laid out in the [CFPB development guidelines](https://github.com/cfpb/development)
- [ ] Future todos are captured in comments and/or tickets
- [ ] Project documentation has been updated, potentially one or more of:
  - [This repo’s docs](https://cfpb.github.io/consumerfinance.gov/) (edit the files in the `/docs` folder) – for basic, close-to-the-code docs on working with this repo
  - CFGOV/platform wiki on GHE – for internal CFPB developer guidance
  - CFPB/hubcap wiki on GHE – for internal CFPB design and content guidance

### Front-end testing

<!--
When new (or significantly modified) front-end functionality is present, the following things should be tested.
Feel free to delete this section if not applicable to this PR.
-->

#### Browser testing

Visually tested in the following supported browsers:
- [ ] Firefox
- [ ] Chrome
- [ ] Safari
- [ ] Edge 18 (the last Edge prior to it switching to Chromium)
- [ ] Internet Explorer 11 and 8 (via emulation in 11's dev tools)
- [ ] Safari on iOS
- [ ] Chrome on Android

<!--
Further guidance on browser support can be found at:
https://github.com/cfpb/development/blob/main/guides/browser-support.md
-->

#### Accessibility

- [ ] Keyboard friendly (navigable with tab, space, enter, arrow keys, etc.)
- [ ] Screen reader friendly
- [ ] Does not introduce new errors or warnings in [WAVE](https://wave.webaim.org/extension/)

#### Other

- [ ] Is useable without CSS
- [ ] Is useable without JS
- [ ] Does not introduce new lint warnings
- [ ] Flexible from small to large screens
