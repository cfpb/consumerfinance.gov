# Installation and Configuration for cfgov-refresh

## 1. Back-end setup

### Virtualenv & Virtualenvwrapper Python modules

Install [Virtualenv](https://virtualenv.pypa.io/en/latest/index.html) and
[virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)
to create a local environment for your server:
```bash
pip install virtualenv virtualenvwrapper
```

### Autoenv module

[Install Autoenv](https://github.com/kennethreitz/autoenv#install) however you’d like.
(We use [Homebrew](http://brew.sh)):

Run:
```bash
brew install autoenv
```

After installation, Homebrew will output instructions similar to:
```bash
To finish the installation, source activate.sh in your shell:
  source /Users/[YOUR MAC OSX USERNAME]/homebrew/opt/autoenv/activate.sh
```

Any time you run the project you’ll need to run that last line. If you’ll be working with
the project consistently, we suggest adding it to your bash profile by running:
```bash
echo 'source /Users/[YOUR MAC OSX USERNAME]/homebrew/opt/autoenv/activate.sh' >> ~/.bash_profile
```

If you need to find this info again later, you can run:
```bash
brew info autoenv
```

> **NOTE:** If you use ZSH you’ll need to use [zsh-autoenv](https://github.com/Tarrasch/zsh-autoenv),
  but we can’t provide support for issues that may arise.

### Elasticsearch

[Install Elasticsearch](http://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html)
however you’d like. (We use [Homebrew](http://brew.sh)):
```bash
brew install elasticsearch
```

Just as with autoenv, Homebrew will output similar instructions after installation:
```bash
To have launchd start elasticsearch at login:
    ln -sfv /Users/[YOUR MAC OSX USERNAME]/homebrew/opt/elasticsearch/*.plist ~/Library/LaunchAgents
Then to load elasticsearch now:
    launchctl load ~/Library/LaunchAgents/homebrew.mxcl.elasticsearch.plist
Or, if you don’t want/need launchctl, you can just run:
    elasticsearch --config=/Users/[YOUR MAC OSX USERNAME]/homebrew/opt/elasticsearch/config/elasticsearch.yml
```

Any time you work on the project, you’ll need to open a new tab and run that last line.
If you’ll be working on the project consistently, we suggest using the first option
utilizing `launchd`.

If you need to find this info again later, you can run:
```bash
brew info elasticsearch
```

### Sheer

To [install Sheer](https://github.com/cfpb/sheer#installation), start by cloning the
Sheer GitHub project to wherever you keep your projects (not inside cfgov-refresh directory):
```bash
git clone https://github.com/cfpb/sheer.git
```

Create a virtualenv for Sheer, which you’ll name `cfgov-refresh`:
```bash
mkvirtualenv cfgov-refresh
```

The new virtualenv will activate right away. To activate it later on
(say, in a new terminal session) use the command `workon cfgov-refresh`.
You’ll know you have a virtual environment activated if you see the name of it in
parentheses before your terminal prompt. Ex:
```bash
(cfgov-refresh)$
```

Install Sheer into the virtualenv with the `-e` flag (which allows you to make changes to
Sheer itself). The path to Sheer is the root directory of the GitHub repository you
cloned earlier, which will likely be `../sheer`:
```bash
pip install -e ~/path/to/sheer
```

Install Sheer’s Python requirements:
```bash
pip install -r ~/path/to/sheer/requirements.txt
```

### GovDelivery

Install the following GovDelivery dependencies into your virtual environment:
```bash
pip install git+git://github.com/dpford/flask-govdelivery
pip install git+git://github.com/rosskarchner/govdelivery
```

> **NOTE:** GovDelivery is a third-party web service that powers our subscription forms.
  Users may decide to swap this tool out for another third-party service.
  The application will function but throw an error if the above GovDelivery values are not set.


## 2. Front-end setup

The cfgov-refresh front-end currently uses the following frameworks / tools:

- [Grunt](http://gruntjs.com): task management for pulling in assets,
  linting and concatenating code, etc.
- [Bower](http://bower.io): Package manager for front-end dependencies.
- [Less](http://lesscss.org): CSS pre-processor.
- [Capital Framework](https://cfpb.github.io/capital-framework/getting-started):
  User interface pattern-library produced by the CFPB.

> **NOTE:** If you’re new to Capital Framework, we encourage you to
  [start here](https://cfpb.github.io/capital-framework/getting-started).

1. Install [Node.js](http://nodejs.org) however you’d like.
2. Install [Grunt](http://gruntjs.com) and [Bower](http://bower.io):

```bash
npm install -g grunt-cli bower
```

## 3. Clone project and install dependencies

Using the console, navigate to your project directory (`cd ~/Projects` or equivalent).
Clone this project’s repository and switch to it’s directory with:

```bash
git clone git@github.com:cfpb/cfgov-refresh.git
cd cfgov-refresh
```

Next, install dependencies with:

```bash
npm install
grunt vendor
```

> **NOTE**: After installing dependencies, rebuild all the site’s assets by running `grunt`.
See the usage section [updating all the project dependencies](README.md#updating-all-dependencies).


## 4. Project configuration

The project uses a number of environment variables. The project uses a WordPress API URL
to pull in content and GovDelivery for running the subscription forms:

- `WORDPRESS` (URL to WordPress install)
- `GOVDELIVERY_BASE_URL`
- `GOVDELIVERY_ACCOUNT_CODE` (GovDelivery account variable)
- `GOVDELIVERY_USER` (GovDelivery account variable)
- `GOVDELIVERY_PASSWORD` (GovDelivery account variable)
- `SUBSCRIPTION_SUCCESS_URL` (Forwarding location on subscription success)

To set these permenantly, copy the `.env-SAMPLE` file and un-comment each variable after
adding your own values. `WORDPRESS` is the only one that’s absolutely necessary to run the site.
```bash
cp .env_SAMPLE .env && open .env
```

If you need to test this project without Autoenv, you can set each of these with:
```
export [CONSTANTNAME]=[CONSTANTVALUE]
```

## 5. Usage

Continue following the [Usage instructions](README.md#usage) in the README.
