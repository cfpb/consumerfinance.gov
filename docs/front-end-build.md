# Building your project's front end

Every CFPB project with a non-trivial front end should:

1. Use **Grunt** or **Gulp** to accomplish all front-end build tasks – [example Gruntfile](https://github.com/cfpb/generator-cf/blob/master/app/templates/grunt/_Gruntfile.js), [example Gulpfile](https://github.com/cfpb/generator-cf/blob/master/app/templates/gulp/_gulpfile.js) and [Gulp scripts](https://github.com/cfpb/generator-cf/tree/master/app/templates/gulp/gulp).
1. Use **Less** as a CSS preprocessor.
1. Use an optional `config.json` file in the project root to store build variables (internal API endpoints, PII, etc.). This file can be consumed by a Grunt/Gulp task and listed in `.gitignore`.
1. Require a maximum of **three commands** to install dependencies and build all static assets:
   1. `npm install`
   1. `grunt build` or `gulp build`
1. These three commands (and any additional commands if there's a strong argument for them) should be stored in a `setup.sh` file ([Grunt example](https://github.com/cfpb/generator-cf/blob/master/app/templates/grunt/_setup.sh), [Gulp example](https://github.com/cfpb/generator-cf/blob/master/app/templates/gulp/_setup.sh)) to make things easier for our CI environments.

You should avoid checking dependencies and minified assets into source control. It's common practice to keep development files in a `src` directory and compiled/minified assets in a gitignored `dist` directory.

## Installing Node

Mac:

```shell
brew install node
```

Linux:

```shell
yum-config-manager --enable epel
yum install nodejs -y
```

## Installing Grunt and Gulp

```shell
npm install -g grunt-cli gulp
```

## Pegging versions

It's good practice to specify specific versions in any dependency management system such as maven, pip, ivy, npm, etc. Yes, it incurs a bit of management overhead in that you have to manually change version numbers when you want to upgrade a dependency. This extra work pays off in absence of time spent tracking down unexpected changes or errors due to a version upgrade of which you were unaware.

When working with npm, we recommend using [npm shrinkwrap](https://docs.npmjs.com/cli/shrinkwrap).

## Building JavaScript and Less

We usually use [Grunt](http://gruntjs.com/) to automate the compilation of JavaScript and Less files. Some projects are transitioning to [Gulp](http://gulpjs.com/). Either is fine.

Here are some helpful plugins for Grunt:

- [grunt-contrib-uglify](https://github.com/gruntjs/grunt-contrib-uglify) for concatenating and minifying JS
- [grunt-contrib-less](https://github.com/gruntjs/grunt-contrib-less) for compiling Less and CSS files
- [grunt-contrib-cssmin](https://github.com/gruntjs/grunt-contrib-cssmin) for minifying CSS
- [grunt-contrib-clean](https://github.com/gruntjs/grunt-contrib-clean) for cleaning folders
- [grunt-contrib-watch](https://github.com/gruntjs/grunt-contrib-watch) for watching and compiling assets on the fly
- [grunt-browserify](https://github.com/jmreidy/grunt-browserify) for using Node style CommonJS modules client-side

## Capital Framework Generator

Our recommended workflow is to use the [generator-cf](https://github.com/cfpb/generator-cf) Yeoman generator to scaffold out a new Capital Framework project. This generator provides a solid front-end build process and directory structure.
