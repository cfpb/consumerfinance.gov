#!/bin/sh
#
# Runtime dependencies, and things expected by Pillow and Wand
# https://github.com/python-pillow/Pillow/blob/master/docs/installation.rst#building-on-macos
# http://docs.wand-py.org/en/0.4.1/guide/install.html#install-imagemagick-on-mac

brew update
brew install docker-compose docker-machine docker imagemagick python node
$(brew --prefix)/bin/pip2.7 install -U pip virtualenv virtualenvwrapper
