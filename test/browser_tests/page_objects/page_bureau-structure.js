'use strict';

function TheBureauStructurePage() {

  this.get = function( ) {
    browser.get( '/the-bureau/bureau-structure/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.orgChartRoot = element( by.css( '.org-chart_root' ) );

  this.directorImage =
  this.orgChartRoot.element( by.css( '.media_image__150' ) );

  this.directorName = this.orgChartRoot.element( by.css( '.h2' ) );

  this.directorTitle = this.orgChartRoot.element( by.css( 'h2' ) );

  this.orgChartBranches = element.all( by.css( '.org-chart_branch' ) );

  this.orgChartParentNodes =
  this.orgChartBranches.all( by.css( '.org-chart_nodes > .org-chart_node' ) );

  this.orgChartChildNodes =
  this.orgChartParentNodes.all( by.css( '.org-chart_node' ) );

  this.downloadInfo =
  element( by.css( '[data-qa-hook="org-chart-download-info"]' ) );

  this.downloadBtn =
  this.downloadInfo.element( by.css( 'a.btn' ) );

  this.speakingInfo =
  element( by.css( '[data-qa-hook="org-chart-speaking-info"]' ) );

  this.speakingInfoEmail = this.speakingInfo.element( by.css( 'a' ) );

}

module.exports = TheBureauStructurePage;
