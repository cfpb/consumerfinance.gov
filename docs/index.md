# Introduction

This is the documentation for the `cfgov-refresh` project, a redesign of the [www.consumerfinance.gov](https://www.consumerfinance.gov) website. It is organized thematically in order to create a central repository for all information pertaining to cfgov-refresh.

# Disclaimer

**This project is a work in progress.** Nothing presented in this repo—whether in the source code, issue tracker, or wiki—is a final product unless it is marked as such or appears on [www.consumerfinance.gov](https://www.consumerfinance.gov). In-progress updates may appear on [beta.consumerfinance.gov](https://beta.consumerfinance.gov).

# Technology stack

The standard technology stack for development of cfgov-refresh within the CFPB consists of the following base:

- Mac OSX
- [Homebrew](https://brew.sh) - package manager for installing system software on OSX
- Python and PIP (Python package manager)
- WordPress API data source URL
- [Jinja templates](http://jinja.pocoo.org) for front-end rendering
- [Wagtail CMS](https://wagtail.io) for content administration
- Dependencies, listed below

# Dependencies

- [Elasticsearch](https://www.elastic.co):
  Used for full-text search capabilities and content indexing.
- [Node](http://nodejs.org) and [npm (Node Package Manager)](https://www.npmjs.com):
  Used for downloading and managing front-end dependencies and assets.

For Vagrant Virtualbox usage (:warning: The Vagrant box is not currently working.)

- [VirtualBox](https://www.virtualbox.org)
- [Vagrant](https://www.vagrantup.com)
- python >=  2.6
- ansible >= 1.9
