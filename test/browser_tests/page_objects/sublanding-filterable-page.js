'use strict';

function SublandingFilterablePage() {

  this.gotoURL = function(url='/sfp') {
    browser.get(url);
  };

  this.results = element.all(by.css('.o-post-preview_content'));
  this.first_result = this.results.first();
  this.last_result = this.results.last();
  this.multiselect = element.all(by.css('.cf-multi-select'));

}

module.exports = SublandingFilterablePage;