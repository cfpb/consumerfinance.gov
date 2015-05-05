All notable changes to this project will be documented in this file.

## How this repo is versioned

We use an adaptation of [Semantic Versioning 2.0.0](http://semver.org).
Given the `MAJOR.MINOR.PATCH` pattern, here is how we decide to increment:

- The MAJOR number will be incremented for major redesigns that require the user
  to relearn how to accomplish tasks on the site.
- The MINOR number will be incremented when new content or features are added.
- The PATCH number will be incremented for all other changes that do not rise
  to the level of a MAJOR or MINOR update.

---------------------------------------

## Unreleased - unreleased

### Added
- Added labels to the phone/email/fax/mail icons on `/contact-us/` page
- Added ability to scrub plural terms in typeAndFilter jQuery plugin
- `.respond-to-retina` mixin for media queries targeting Retina iOS devices
- Scroll to top functionality on footer
- Added `/modules/util/web-storage-proxy.js` utility module.
- Added `/modules/util/js-loader.js` utility module.

### Changed

- Updated mailing addresses in `/contact-us/` sidebar
- Added `browserify` package and its dependencies
  and refactored codebase to use Browserify for JS modules.
- Added additional ESLint option flags in `space-in-brackets` rule.
- Added ability to scrub plural terms in typeAndFilter jQuery plugin
- Changed ESLint indent amount to 2 spaces to match CFPB front-end standards.
- Turns off ESLint `func-names` setting because its too verbose for the gain it provides.
- Updated `grunt` to `~0.4.5`.
- Updated `jquery` to `^1.11.3`.
- Replaced `grunt-uglify` with `uglifyify`.
- Updated mailing addresses in `/contact-us` sidebar
- Reverted navs from Contact Us redacting
- Updated footer to match new designs
- Refactored email subscribe form

### Fixed
- Improvements and fixes to `/contact-us/` page


## 3.0.0-0.3.0 - 2015-04-23

### Added
- Added Privacy Policy page.
- Added Event Request a Speaker page.
- Added settings to enable the `/blog/` and `/newsroom/` RSS feeds.
- Added `brand-palette.less` and `cf-theme-overrides.less`.
- Added `block__border` to `cf-enhancements.less` to provide borders around blocks.
- Added alert to form validation failure
- Added .env config for easier project setup
- Added Event processor

### Changed
- Added styles to 500 and 404 error pages.
- Updated content on 500 and 404 error pages.
- Added full width button modifier for buttons on smaller screens.
- Updated ESLint configuration to the latest ESLint release (v0.18.0).
- Updated `/newsroom/` and `/blog/` post sidebars to add description
  and date, and to update styles.
- Updated icons to use livestream icon instead of wifi icon.
- Updated blog post spacing to be consistent with overall-project spacing.
- Updated round step-by-step slug icons to central-align numbers.
- The name "Watchroom" to "Featured Topic"
- Updated cf-buttons to 1.4.2.
- Updates cf-layout to 0.3.0.
- Changed block background to 5% gray.
- Updated contact us content
- Improved Elasticsearch mappings
- Improved README and INSTALL docs

### Fixed
- Updated related links module on `/newsroom/`.
- Added small screen styles to helpful terms vertical list
  on `/contact-us/` page.
- Updated multi-line icon list styles.
- Fixed missing `jump-link__right` modifier from `/featured-topic.html`.
- Fixed an issue within `/newsroom/` and `/activity-log/` filters where selecting "Blog"
  and another category would return zero results.
- Fixed issue in filters where an input whitespace would prevent suggestions from showing.
- Fixed HTML, typos, and grammatical errors.
- Fixed line height issue in Chosen select boxes
- Updated Google Tag Manager ID from testing account to production account.
- Fixed whistleblower slug on contact us


## 3.0.0-0.2.3 - 2015-03-23

### Changed
- Updated events to match design
- Updated markup with new Isocons
- Updated email form to remove topics
- Updated footer to match new design
- Updated content throughout site
- Updated less files to cleanup code

### Fixed
- Fixed filtering when partial dates are used
- Updated processors to match WordPress API output
- Added sub-nav for mobile devices in instances where hero is present
- Added breakpoint range for main nav on med sized device screens
- Updated the expandable layout for multiple lines of text
- Updated list icons for multiple lines of text
- Added titles to pages that were missing them
- Updated broken links
- Lots more typos


## 3.0.0-0.2.2 - 2015-03-17

### Added
- New Events Archive landing page (with borrowed post data)
- New Events Archive detail page (with borrowed post data)
- New eslint settings file

### Changed
- Updated archived events landing page to display events, filters and pagination
- Updated the Gruntfile for eslint over jshint
- Switched from ElasticSearch queries to filters
- Updated form macro layout to account for optional content
- Updated macro arguments for clearer conditions
- Updated events list for new CF media block
- Updated static content
- General code cleanup

### Fixed
- Events filter showing no results text while displaying found results
- Settings file for PDFReactor
- JS errors
- General layout issues
- Lots of typos


## 3.0.0-0.2.1 - 2015-03-03

### Added
- New Upcoming Events landing page (with borrowed post data)
- New Upcoming Event detail page (with borrowed post data)
- Created new table modifier for simple small screen tables


## 0.2.0 - 2014-12-29

Apologies for ignoring our versioning for five months.

### Added
- Newsroom, Contact Us, About the Bureau, Offices, Doing Business with Us,
  Activity Log, and Budget sections.
- Many new design patterns.
- Tests

### Changed
- Significant template structure overhaul.

### Fixed
- Tons of stuff.


## 0.1.0 - 2014-07-14

Initial release. Contains fully functioning blog section.
