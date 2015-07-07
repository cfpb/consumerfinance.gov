function careers_studentsAndGraduates() {
  this.get = function() {
    browser.get( '/careers/students-and-graduates/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };
  this.opportunities = element.all( by.css( '.careers-students-and-graduates h2' ) );
}

module.exports = careers_studentsAndGraduates;