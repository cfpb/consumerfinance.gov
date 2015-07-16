'use strict';

function StudentsAndGraduates() {
  this.get = function() {
    browser.get( '/careers/students-and-graduates/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };
  this.opportunities = element.all( by.css( '.careers-students-and-graduates .content_main .media h2' ) );
}

module.exports = StudentsAndGraduates;
