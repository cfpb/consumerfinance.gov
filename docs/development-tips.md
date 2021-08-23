# Development tips


## Main front-end template/asset locations

**Templates** that are served by the Django server: `cfgov/jinja2/v1`

**Static assets** prior to processing (combilation, minification, etc.):
`cfgov/unprocessed`.

!!! note
    After running `gulp build` (or `./setup.sh`) the site's assets are copied over to `cfgov/static_built`,
    ready to be served by Django.


## Installing new front-end dependencies

- Use `yarn add new_dep@se.m.ver` to install new dependencies
  or update existing dependencies.
- If you can't do this for some reason or are looking to freshen all dependencies,
  you will need to edit `.yarnrc`, temporarily commenting out the `--install.pure-lockfile true`
  and `--install.offline true` flags before proceeding with your installation or update.
- In the rare but observed case that `yarn add new_dep@se.m.ver` doesn't add
  every needed package to the offline cache, you likely need to first run
  `yarn cache clean`.

## Watching files for changes

Some (but not all) JavaScript and CSS files can be rebuilt automatically when they are changed by using `gulp watch` or `yarn run gulp watch`.

!!! note
    You must build the assets first, so you may want a command like: 
    ```
    ./setup.sh docker && yarn run gulp watch
    ```


## Developing on nested satellite apps

Some projects can sit inside consumerfinance.gov, but manage their own asset
dependencies. These projects have their own `package.json` and base templates.

The structure looks like this:

### npm modules
- List an app's own dependencies in
  `cfgov/unprocessed/apps/[project namespace]/package.json`.

### Webpack
- Apps may include their own `webpack-config.js` configuration that adjusts how
  their app-specific assets should be built. This configuration appears in
  `cfgov/unprocessed/apps/[project namespace]/webpack-config.js`.

### Browserslist
- Apps may include a
  [browserslist config](https://github.com/browserslist/browserslist#config-file)
  file, which is automatically picked up by `@babel/preset-env` inside the
  webpack config, if no `browsers` option is supplied.

### Adding Images
- Images should be compressed and optimized before being committed to the repo
- In order to keep builds fast and reduce dependencies, the front-end build does not contain an image optimization step
- A suggested workflow for those with Adobe Creative Suite is as follows:
  1. Export a full-quality PNG from Adobe Illustrator
  1. Reexport that PNG from Adobe Fireworks as an 8-bit PNG
  1. Run the 8-bit PNG through [ImageOptim](https://imageoptim.com)

### Templates
- Apps use a Jinja template that extends the `base.html`
  template used by the rest of the site.
  This template would reside in `cfgov/jinja2/v1/[project namespace]/index.html`
  or similar (for example, [owning-a-home](https://github.com/cfpb/consumerfinance.gov/blob/main/cfgov/jinja2/v1/owning-a-home/explore-rates/index.html)).

!!! note
    A template may support a non-standard browser, like an older IE version,
    by including the required dependencies, polyfills, etc. in its
    template's `{% block css %}` or `{% block javascript scoped %}` blocks.
