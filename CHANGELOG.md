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

## Unreleased

### Added
- Added Favicon
- New and improved primary nav (both look and interaction)
- Added expanded-state utility for getting/setting aria-expanded
- Added Acceptance tests for the `activity-log` page.
- Added webpack module loader for per-page JavaScript.
- Added external-site page-specific script.
- Added `config/environment.js` for project JS path configuration.
- Added filesystem helper to gulp utilities for retrieving a binary executable.
- Django Server
- Django related urls to access links
- Django-Sheerlike integration
- Added Acceptance tests for `the-bureau` pages.
- Added test utility to retreive QA elements.
- Added ARIA state utility to enable decorating dom elements with ARIA states.
- Added `Object.defineProperty` polyfill.
- Added unit test for `aria-state.js`.

### Changed
- Updated Video Code to make it usable on Events pages.
- Changed gulp JS unit testing task from `gulp:unit:js` to `gulp:unit:scripts`
- Updated Meredith Fuchs bio and images.
- Added indent rules for `var`, `let`, and `const` in ESLint config file.
- Replaced old Grunt legaccsy plugin with Gulp mq-remove plugin
- Added ability for acceptance --specs test flag to accept list of test files.
- Changes `big_radio` macro to `radio_big` and `checkbox_bg` to `checkbox_big`.
- Updated the primary nav to move focus as user enters and leaves nav levels
- Moved handlebars from npm to bower.
- Added jQuery CDN with fallback to head to satisfy GTM requirements.
- Changes the location of the /dist folder to cfgov/v1/jinja2/v1
- Server port is now at 8000

### Removed
- Disables tests for landing page events, since we don't currently have events.
- Removed unused exportsOverride section,
  which was an artifact of the grunt bower task.
- Removed browserify, watchify, and browserify-shim dependencies.

### Fixed
- Fixed issue with logic displaying the Event summary state.
- Fixed missing IE only stylesheet for older systems/browsers.
- Fixed skip-navigation link for keyboard navigation.
- Fixed instructions for gulp watch
- New way to run the server documented in the INSTALL.MD
- New way to define url routing, no longer automatically set by file path

## 3.0.0-2.3.0 - 2015-08-27

### Added
- Added time macro.
- Added `gulp test:unit` and `gulp test:acceptance` tasks for test stages.
- Added support for link buttons to disabled link utility class.
- Added `breakpoints-config.js` config file to use for responsive JS.
- Added breadcrumbs to blog, newsroom, careers, business, bureau
  and budget pages
- Added Meredith Fuchs to Leadership calendar filter.
- Added unit test for `assign` utility.
- Added `get-breakpoint-state.js` to add support for responsive JS.

### Changed
- Moved `.meta-header`, `.jump-link`,
  and `.list__links` to `cf-enhancements.less`.
- Converted time elements to use time template.
- Broke apart format macros into topical macros.
- Updated legacy code to remove old jQuery dependency and
  unnecessary code.
- Updated copy on `about-us` page
- Added copying of `.env_SAMPLE` to `.env` part of `setup.sh`.
- Moved console output messages to the end of the `setup.sh` `init` method.
- Organized `.env_SAMPLE` and made `.env` executable on its own.
- Added `HTTP_HOST`, `HTTP_PORT`, `SELENIUM_URL`, `SAUCE_USERNAME`,
  `SAUCE_ACCESS_KEY`, `SAUCE_SELENIUM_URL`, and `VIRTUAL_ENV`
  constants to `.env_SAMPLE`.
- Moved aggregate `gulp lint` task to bottom of file to avoid duplicate
  lint task entries in `gulp --tasks`.
- Renamed `gulp lint:src` to `gulp lint:scripts` to future-proof type of linting.
- Renamed `gulp test:macro` to `gulp test:unit:macro`.
- Renamed `gulp test:processor` to `gulp test:unit:processor`.
- Renamed `gulp test:browser` to `gulp test:acceptance:browser`.
- Edited `INSTALL.md` to accommodate changes in `.env_SAMPLE`.
- Edited Protractor configuration to include browser groups,
  which by default only run the essentials locally, but the full suite
  (including legacy browsers) on Sauce Labs when Sauce credentials are present.
- Updated test instructions to use the gulp test subtasks.
- Updated Travis CI settings to use `setup.sh`.
- Updated files to use `breakpoints-config.js`.
- Made `/the-bureau/bureau-structure/role-macro.html` private.
- Updated `gulp clean` to leave the `dist` directory and remove the inner
  contents
- Use `HTTP_PORT` environment variable for port in `gulp watch`, if available.
- Removed "optional" text from privacy complaint form
  and added `*` to designate required fields.
- Updated Deputy Director information to Meredith Fuchs.
- Updated `/about-rich-cordray/` URL to `/about-director/`.
- Updated `/about-meredith-fuchs/` URL to `/about-deputy-director/`.
- Normalized director and deputy director photos to be format `NAME-WxH.jpg`.
- Changed name of `shallow-extend` utility to 'assign'.
- Superscripts `st` in `21st` on About Us page.
- Updated `BreakpointHandler.js` to support usage of `breakpoints-config.js`.

### Removed
- Removed styles from codebase that have already been migrated
  to cf-typography.
- Removed duplicate Privacy Policy
- Removed processor tests due to them being outdated.
- Removed failing bureau tests to be debugged later

### Fixed
- Fixed borders on sub-footers across the website
- Fixed 'Return to top' button width on footer
- Fixed default gulp task
- Fixed icon links to match CFPB Design Manual
- Fixed gulp copy task that was missing copying PDFs in subdirectories.
- Fixed issues with active filter logic.
- Fixed testing issue with single pages reloading for every test
- Fixed testing timeouts the first fix didn't correct by updating timeout time


## 3.0.0-2.2.0 - 2015-08-18

### Added
- Transitioned Capital Framework dependency to v1.0.0 in bower.json.
- Added gulp and the required npm plugins
- Added gulp config file to lay out configs for each task
- Added gulp tasks split up into their own files
- Added acceptance tests for `/offices/*` pages accessible through site's menu.
- Added Accessibility page to footer and adds Accessibility page tests.
- Added acceptance tests for `/sub-pages/*`.
- Added `activities-block` shared template for activity feed
  on offices and sub-pages.
- Added accessibility complaint form.
- Added "File an EEO Issue" form.
- Added `/offices/office-of-civil-rights/` page, tests, and link in footer.

### Changed
- Site's "About" text to "About Us".
- Replaced FOIA Records with Coming Soon heading
- Updated setup.sh to use gulp
- Updated travis to use gulp tasks
- Updated main.less to use the paths option in less compiler.
- Moved and renamed contact-macro to contact-layout in macros directory.
- Moved filters macro from `post-macros.html` to `/macros/filter.html`.
- Made filters macro helpers private.
- Moved getViewportDimensions out of utilities.js and into own module.
- Updated ESLint to v1.0.0.

### Removed
- Removed Grunt plugins from package.json
- Removed the Gruntfile.
- Removed homepage progress charts and related content and JS.
- Removed 80px to 120px sizing for the isocon sizes on the-bureau page.
- Removed cf-pagination and other unused JS.

### Fixed
- Fixed margins on site footer.
- Switched the two forms under Privacy to their correct positions
- Fixed incorrect email href reference on offices contact email link.


## 3.0.0-2.1.0 - 2015-08-05

### Added
- Added `sub-pages/civil-penalty-fund-allocation-schedule/` page.
- Added `sub-pages/sub-pages/consumer-education-financial-literacy-programs/` page.
- Added `u-hidden` utility class for fully hiding an element.
- Added `TEST.md` readme file for testing instructions.
- Added `grunt clean` and `grunt copy` tasks.
- Added `grunt clean` step to `setup.sh`.
- Added `map` and `filter` array polyfills.
- Added `about-us` page and tests
- Added `newsroom` type to Activity Snippets
- Created initial career posting template.
- Created 1/4 and 3/4 layout columns.
- Added DL styles to cf-enhancements.
- Added `offices/project-catalyst`.
- Careers processor/mapping/query.
- Added `office_[office slug]` class to offices template.
- Careers to the lookups.py
- Added `media_image__150` modifier for 150 pixel wide images.
- Added `simple-table-row-links.js` for making tables with linkable rows.
- Added `event-listener.js` and `query-selector.js` polyfills for IE8.
- Added `@tr-border` variable to `cf-enhancements.less`
  for simple-table border color.
- Added tests for events and event archive landing pages

### Changed
- Updated primary navigation to match new mega menu design.
- Changed project architecture to having `/src/` and `/dist/` directory.
- Changed `/_tests/` directory name to `/test/`.
- Changed `/_tests/macro_testing` directory name to `/test/macro_tests`.
- Moved `browserify-shims.js` to `/config/` directory.
- Upgraded Travis to container-based infrastructure
- Updated Offices pages to change activity feed logic.
- Updated block-bg padding in cf-enhancements based on JJames feedback.
- Updated Offices sub pages to display related documents.
- Updated Offices sub pages to always display activity feed.
- Updated Expandable macro to update design and add FAQ options.
- Moved `sub-page_[sub-page slug]` class to main content area of sub_pages template.
- Styled unordered lists as branded lists in the `office_intro-text`,
  `sub-page_content`, and `sub-page_content-markup` class areas.
- Updated all careers images to 2x size and have the same markup structure.
- Updated event macros to use Sheer 'when' function in order to
  display content based on state.
- Tied careers data into single template and renamed to _single.html
- Replaced career pages mock jobs data with data from the jobs API.
- Made jobs list table on /careers/current-openings/ have linkable rows.
- Adds eslint ignore lines for polyfills, which will not be changing.
- Moved CF table color overrides to `cf-theme-overrides.less`.
- Updated the existing missions browser test to be stronger
- Updated the browser test specs in conf.js because the shared spec was being
  fired on the desktop test, even though those tests had already been run in
  Chrome. Now the desktop test only runs the desktop spec.
- Separated `grunt test` task from `grunt build`
  and made default task test + build.

### Removed
- Removed requestAnimationFrame polyfill.
- Removed `_tests/browser_tests/README.md`, `_tests/macro_testing/README.md`, `_tests/processor_tests/README.md`.
- Removed `grunt vendor` from `setup.sh`.
- Removed unused CSS on `office.less`
- Removed `/events/archive/_single.html`

### Fixed
- Fixed issue on IE11 when using the dates to filter caused
  by toString method.
- Event tag filtering on archive page
- Added browser tests to linting task
- Fixed MobileOnlyExpandable error on office page.
- Normalized use of jinja quotes to single quote
- Fixed a large chunk of the existing linting errors and warnings
- Fixed issue with active filters on`/the-bureau/leadership-calendar/print/` page.


## 3.0.0-2.0.0 - 2015-07-24

### Added
- Added `sub-pages/civil-penalty-fund-allocation-schedule/` page.
- Added `sub-pages/sub-pages/consumer-education-financial-literacy-programs/` page.
- Added `u-hidden` utility class for fully hiding an element.
- Added `TEST.md` readme file for testing instructions.
- Added `grunt clean` and `grunt copy` tasks.
- Added `grunt clean` step to `setup.sh`.

### Changed
- Updated primary navigation to match new mega menu design.
- Changed project architecture to having `/src/` and `/dist/` directory.
- Changed `/_tests/` directory name to `/test/`.
- Changed `/_tests/macro_testing` directory name to `/test/macro_tests`.
- Moved `browserify-shims.js` to `/config/` directory.

### Removed
- Removed requestAnimationFrame polyfill.
- Removed `_tests/browser_tests/README.md`,
  `_tests/macro_testing/README.md`, `_tests/processor_tests/README.md`.
- Removed `grunt vendor` from `setup.sh`.

### Fixed
- Fixed issue on IE11 when using the dates to filter caused
  by toString method.
- Event tag filtering on archive page


## 3.0.0-1.3.0 - 2015-07-16

### Added
- Added `block__border-left` and `block__border-right` CF enhancements.
- Added `students-and-graduates` page to careers section.
- Added `short_title` to Office/Subpage.
- Added ordering to the navigation on Office/Subpage.
- Added script to index all links on our site.
- Added initial browser test with instructions for testing and adding more
- Added `media_image__100` and `media_image__130-to-150` classes for responsive
  image sizes on mobile carousel.
- Added `u-link__disabled` utility class for styling disabled links.
- Added `/careers/working-at-cfpb/` page.
- Added block templates for LinkedIn info, provide feedback link,
  and career page summaries.
- Added `MobileCarousel.js` module for instantiating the slick carousel
  and added associated `js-mobile-carousel` class as a hook.
  Also added `mobile-carousel` for CSS.
- Added `the-bureau` page wrapper class.
- Added `media-stack` CSS block for stacked media objects.
- Added fixes for `open-government` pages.
- Added `careers/application-process` page.
- Support in Event processor for ICS file generator
- Added `careers/current-openings` page.
- Added `/transcripts/` folder and transcript for job application video
- Added Google Maps image utility macro
- Added `careers/` landing page.
- Added options for toggling each network icon in share macro
- Added LinkedIn sharing (toggled off by default) in share macro

### Changed
- Fixed background and border on secondary navigation.
- Related Links now disable styles links with empty URLs.
- Updated secondary navigation to use true parent/child relationships.
- Events processor/mapping/queries for new Event type structure.
- Changed the way navigation works for Office/Subpage.
- Updated grunt-eslint to version 16.0.0 and updated ESLint config to latest.
- Moved modules that can be instantiated through the `new` keyword
  to a `classes` subdirectory.
- Moved page-sniffing JS code to page scripts for the-bureau
  and working with the CFPB pages.
- Moved carousel to a macro and implemented on the-bureau
  and working at the CFPB pages.
- Moved MobileOnlyExpandable initialization out of MobileCarousel.
- Converted excerpts HTML to articles from sections in the careers section.
- Breaks `macros.html` apart into files in the /macros/ directory.
- Updated events templates to match new data and processor.
- Updated percentages based on recent updates.
- Updated activities_snippet macro to make column markup dynamic.
- Replaced placeholder images on /careers/working-at-cfpb/
- Updated footer to add offices links.
- Moved the disperate arguments into one main options argument with
  key: val pairs for each option in share macro
- Updated email sharing to use mailto: link instead of addthis network
  (removes need for the external privacy notification and consolidates
  email patterns) in share macro

### Removed
- Removed `list_link__disabled` class.
- Removed is_mobile macro and logic from filter.

### Fixed
- Fixed contact-us templates to make them private.
- Fixed issue displaying grandchild pages on sub-pages.


## 3.0.0-1.2.2 - 2015-07-02

### Added

### Changed

### Removed

### Fixed
- Office/Subpage navigation links on beta
- Ordering of subpages in the nav on Office page

## 3.0.0-1.2.1 - 2015-06-29

### Removed
- Event processor to fix indexing error


## 3.0.0-1.2.0 - 2015-06-19

### Added
- Added `setup.sh` script for bootstrapping the project.
- Added insertTarget and insertLocation options to cf_notifier plugins
- Added `box-sizing-polyfill` to `exportsOverride` as needed for
  `grunt-bower-task` to work correctly. `box-sizing-polyfill`
  is installed by cf-grid.
- Added `grunt watch:js` task for completeness.
- Added vendor directory variable to `main.less`.
- Added warning for concat:cf-less Grunt task when sourcefiles are missing.
- Added form for Submit a request FOIA page
- Added styles, JavaScript for hiding and showing additional fields in forms
- Added toplevel navigation items config file for removing hardcoded
  navigation menu items.
- Added external url redirect page, styles, and JavaScript.
- Added `.nav-secondary_link__disabled` style.
- Added `.nav-secondary_item__child` class to visually distinguish sub-pages
  from sibling pages in the sidenav.
- Added `.nav-secondary_item__parent` class to visually distinguish browse
  pages from the subpages below them in the sidenav.
- Added JavaScript utilities for checking types and primitives.
- Added `primary_nav` jinja block to `base.html` template.
- Added FAQ processor and mapping
- Added `use_form` field to sub_pages
- Added `related_faq` field to sub_pages and offices
- Added `inset-divider` class for providing an inset horizontal rule
  independent of the list or list item widths within the side navigation bar.
- Added `preview_text` and `short_title` fields to sub_pages.
- Added `templates/activities-feed.html` HTML template for the activity feed
  area on the offices and sub_pages.
- Added Plain Writing Feedback form.
- Added `cfpb_report` activity type to activities feed macro.
- Added breadcrumbs macro and temporarily set breadcrumbs for all office sub-pages.
- Added download icons to `privacy-impact-assessments-pias`

### Changed
- Relaxed ESLint `key-spacing` rule to warning.
- Refactored breakpoint-handler module into separate class modules
  and utility function.
- PascalCase ContentSlider module to properly designate class status.
- Reduced complexity of validation and notification plugins
- Changed vendor directory to `src/vendor` and updated paths.
- Changed to using `jit-grunt` in place of `load-grunt-tasks`.
- Updated contact us filter to use new notifications
  (replacing type-and-filter messaging with cf_notifier)
- Replaced placeholder Activity Feed on FOIA faq page with actual Activity Feed
- Sped up notification animations
- Added custom template for FOIA records page.
- Refactored code for Wordpress updates
- Initiatives renamed to Sub-pages
- Relaxed ESLint cyclomatic `complexity` rule to max 4 complexity.
- Updates megamenu bureau title to "The Bureau" to fit with sitemap direction.
- Moved Less files to `/src/static/css/` directory.
- Updated `cf-icons` to 0.6.0.
- Update processors.py for FAQ
- Moved HTML templates to `/templates/` subdirectory.
- Breaks header template apart into `header.html`
  and `primary-nav.html` templates.
- Moved external site page header to its own template
  `header-without-nav.html`.
- Minor codefixes on `show-hide-fields.js` along with changing a class name for hiding fields
- Updated side navigation bar to keep page order at mobile sizes and adds
  "IN THIS SECTION" header text to the navigation bar dropdown menu.
- Updated processors to use Elasticsearch bulk indexing
- Office and sub-pages activity feed title to "Latest Activities"
  and contacts to "Contact Information."
- Moved `activity_snippets` macro from `post-macros.html` to `macros/activity-snippet.html`
  and adds render method.
- Made `activity_snippet` macro private.
- Moved `category_icon` macro from `post-macros.html` to `macros/category-icon.html`
  and adds render method.
- Moved `string_length` macro from `macros.html` to `macros/util/text.html`.

### Fixed
- Fixed an issue where scripts were being initialized out of order
- Fixed most of the warnings in validation and notification plugins
- Fixed processor name bug
- Fixed template/processor bugs while indexing and rendering
- Fixed FOIA pages from the template/processor changes
- Fixed missing states from `.nav-secondary_link__disabled` class for
  visited and active links.
- Fixed missing sidebar

### Removed
- Removed `copy:static-legacy` and `grunt-contrib-copy` package.
- Removed unneeded entries from `exportsOverride` in `bower.json`.
- Gitignored CF fonts, "chosen" images, and other vendor files from repo,
  which are slated for eventual removal.
- Removed unused `nav-secondary.html` template.
- Removed unused `cf_inputSplit.js` js module.


## 3.0.0-1.1.0 - 2015-05-20

### Added
- Added `--quiet` grunt CLI flag for suppressing linter warnings.
- Added JS unit testing and code coverage through Mocha and Istanbul.
- Added cf-notifications stylesheet to style notifications
- Added cf_notifier plugin for sending UI notifications
- Added cf_formValidator plugin for validating form inputs
- Added Grunt `build` task and set it as default.
- Added hero and YouTube video functionality to the '/the-bureau/' page.
- Added ajax subscription submission.
- Initiative folder and files for Initiative pages
- Added custom template for FOIA faqs page

### Changed
- Updated grunt-browserify to `^3.8.0`.
- Updated grunt-eslint to `^13.0.0`.
- Moved eslint config file to home directory.
- Moved jQuery download to package.json.
- Updated grunt-banner to `^0.4.0` and updates banner ascii art and format.
- Changed bower.json authors array field to use `homepage` in place of `url`,
  and adds `email` field.
- Adds path variables to Gruntfile.
- Updated form-validation script to use cf_formValidator and cf_notifier
- Changed Grunt `jsdev` and `cssdev` to `js` and `css`.
- Moved testing to build task.
- Updated 404 image to the latest image provided by the design team.
- Office folder and files for Office pages
- Updated template for office pages

### Fixed
- Fixed macro on offices page template
- Fixed subscribe macro in events archive and archive single, and press resources
- Sheer indexing error when related posts are deleted
- Office and Initiative processors
- Slick carousel site-wide JS error.
- Fixed issue with some contacts not showing phone numbers and email addresses

### Removed
- Removed string-replace:static-legacy Grunt task.
- Alert.js plugin
- alert macro
- Unused index.html file from /initiatives/
- Unnecessary setting of template variables


## 3.0.0-1.0.1 - 2015-05-18

### Fixed
- Replaced missing string_score library for the type-and-filter plugin

## 3.0.0-1.0.0

### Added
- Added labels to the phone/email/fax/mail icons on `/contact-us/` page
- Added ability to scrub plural terms in typeAndFilter jQuery plugin
- `.respond-to-retina` mixin for media queries targeting Retina iOS devices
- Scroll to top functionality on footer
- Added `/modules/util/web-storage-proxy.js` utility module.
- Added `/modules/util/js-loader.js` utility module.
- Adds ESLint check for `@todo` jsdoc syntax.
- Updated ESLint configuration to match version `0.20.0.`
  Adds enforcement of `no-dupe-args` and `no-duplicate-case` rules,
  and warnings for `no-continue` and `operator-linebreak` rules.
- Adding mocha tests to `grunt test`

### Changed

- Updated mailing addresses in `/contact-us/` sidebar
- Added `browserify` package and its dependencies
  and refactored codebase to use Browserify for JS modules.
- Added additional ESLint option flags in `space-in-brackets` rule.
- Changed ESLint indent amount to 2 spaces from 4 to match CFPB front-end standards.
- Turns off ESLint `func-names` setting because it's too verbose for the gain it provides.
- Added ability to scrub plural terms in typeAndFilter jQuery plugin
- Updated `grunt` to `~0.4.5`.
- Updated `grunt-eslint` to version `12.0.0.`
- Updated `jquery` to `^1.11.3`.
- Replaced `grunt-uglify` with `uglifyify`.
- Updated mailing addresses in `/contact-us` sidebar
- Reverted navs from Contact Us redacting
- Updated footer to match new designs
- Refactored email subscribe form

### Fixed
- Improvements and fixes to `/contact-us/` page


### Removed

- Removed demo text suffix from page titles.


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
