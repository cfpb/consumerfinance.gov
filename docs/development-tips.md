## Development tips

### TIP: Developing on nested satellite apps
Some projects can sit inside cfgov-refresh, but manage their own asset
dependencies. These projects have their own package.json and base templates.

The structure looks like this:

#### npm modules
- App's own dependency list is in
  `unprocessed/apps/[project namespace]/package.json`
- App's `node_modules` path is listed in the Travis config
  https://github.com/cfpb/cfgov-refresh/blob/master/.travis.yml#L10
  so that their dependencies will be available when Travis runs.

#### Webpack
- Apps may include their own webpack-config.js configuration that adjusts how
  their app-specific assets should be built. This configuration appears in
  `unprocessed/apps/[project namespace]/webpack-config.js`

#### Browserlist
- Apps may include a
  [browserlist config](https://github.com/browserslist/browserslist#config-file)
  file, which is automatically picked up by `@babel/preset-env` inside the
  webpack config, if no `browsers` option is supplied.

#### Adding Images
- Images should be compressed and optimized before being committed to the repo
- In order to keep builds fast and reduce dependencies, the front-end build does not contain an image optimization step
- A suggested workflow for those with Adobe Creative Suite is as follows:
  - Export a full-quality PNG from Adobe Illustrator
  - Reexport that PNG from Adobe Fireworks as an 8-bit PNG
  - Run the 8-bit PNG through [ImageOptim](https://imageoptim.com)

#### Templates
- Apps use a jinja template that extends the `base.html`
  template used by the rest of the site.
  This template would reside in `cfgov/jinja2/v1/[project namespace]/index.html`
  or similar (for example, [owning-a-home](https://github.com/cfpb/cfgov-refresh/blob/master/cfgov/jinja2/v1/owning-a-home/explore-rates/index.html)).

!!! note
    A template may support a non-standard browser, like an older IE version,
    by including the required dependencies, polyfills, etc. in its
    template's `{% block css %}` or `{% block javascript scoped %}` blocks.

### TIP: Working with the templates

#### Front-End Template/Asset Locations

**Templates** that are served by the Django server: `cfgov\jinja2\v1`

**Static assets** prior to processing (minifying etc.): `cfgov\unprocessed`.

!!! note
    After running `gulp build` the site's assets are copied over to `cfgov\static_built`,
    ready to be served by Django.
