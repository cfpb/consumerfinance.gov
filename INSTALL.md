# 1. Back-end setup

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

## Back-end environment variables

The project needs a number of environment variables.
The project uses a WordPress API URL to pull in content
and GovDelivery for running the subscription forms:

- `WORDPRESS` (URL to WordPress install)
- `GOVDELIVERY_BASE_URL`
- `GOVDELIVERY_ACCOUNT_CODE` (GovDelivery account variable)
- `GOVDELIVERY_USER` (GovDelivery account variable)
- `GOVDELIVERY_PASSWORD` (GovDelivery account variable)
- `SUBSCRIPTION_SUCCESS_URL` (Forwarding location on Subscription Success)

> You can also export the above environment variables to your `.bash_profile`,
or use your favorite alternative method of setting environment variables.

**NOTE:** GovDelivery is a third-party web service that powers our subscription forms.
Users may decide to swap this tool out for another third-party service.
The application will function but throw an error if the above GovDelivery values are not set.


# 2. Front-end setup

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

# 3. Clone project and install dependencies

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

> Note: After installing dependencies,
rebuild all the site's assets by running `grunt`.
See the usage section
[updating all the project dependencies](README.md#updating-all-dependencies).
