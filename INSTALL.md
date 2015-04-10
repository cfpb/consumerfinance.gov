### 1. Back-end setup

Follow the [Sheer installation instructions](https://github.com/cfpb/sheer#installation)
to get Sheer installed.
**NOTE:** We suggest creating a virtualenv variable specific to this project,
such as `cfgov-refresh` instead of `sheer` used in the Sheer installation instructions:

```bash
$ mkvirtualenv cfgov-refresh
```

Install the following dependencies into your virtual environment.
We called ours `cfgov-refresh` (see previous step above):

```bash
$ workon cfgov-refresh

$ pip install git+git://github.com/dpford/flask-govdelivery
$ pip install git+git://github.com/rosskarchner/govdelivery
```

### 2. Front-end setup

The cfgov-refresh front-end currently uses the following frameworks / tools:

- [Grunt](http://gruntjs.com): task management for pulling in assets,
  linting and concatenating code, etc.
- [Bower](http://bower.io): Package manager for front-end dependencies.
- [Less](http://lesscss.org): CSS pre-processor.
- [Capital Framework](https://cfpb.github.io/capital-framework/getting-started):
  User interface pattern-library produced by the CFPB.

**NOTE:** If you're new to Capital Framework, we encourage you to
[start here](https://cfpb.github.io/capital-framework/getting-started).

1. Install [Node.js](http://nodejs.org) however you'd like.
2. Install [Grunt](http://gruntjs.com) and [Bower](http://bower.io):

```bash
$ npm install -g grunt-cli bower
```

### 3. Clone project and install dependencies

Using the console, navigate to your project directory (`cd ~/Projects` or equivalent).
Clone this project's repository and switch to it's directory with:

```bash
$ git clone git@github.com:cfpb/cfgov-refresh.git
$ cd cfgov-refresh
```

Next, install dependencies with:

```bash
$ npm install
$ grunt vendor
```

### 4. Updating all dependencies

Each time you fetch from the upstream repository (this repo),
you should install and update dependencies with npm and `grunt vendor`,
and then run `grunt` to rebuild all the site's assets:

```bash
$ npm install
$ npm update
$ grunt vendor
$ grunt
```
