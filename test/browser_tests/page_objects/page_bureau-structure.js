'use strict';

function TheBureauStructurePage() {

  this.get = function( ) {
    browser.get( '/the-bureau/bureau-structure/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.secondaryNavigation = element( by.css( '.o-secondary-navigation' ) );

  this.orgChartRoot = element( by.css( '.org-chart_node__root' ) );

  this.orgChartCategoryLinks =
    element.all( by.css( '.org-chart_categories .link_item' ) );

  this.orgChartBranches = element.all( by.css( '.org-chart_branch' ) );

  this.orgChartParentNodes =
    this.orgChartBranches.all(
      by.css( '.org-chart_nodes > .org-chart_node' )
    );

  this.orgChartChildNodes =
    this.orgChartParentNodes.all( by.css( '.org-chart_node' ) );

  this.downloadInfo =
    element( by.css( '[data-qa-hook="org-chart-download-info"]' ) );

  this.downloadBtn =
    this.downloadInfo.element( by.css( 'a.btn' ) );

  this.getExpandableOffice = function() {
    return element( by.css( '.slick-slider .o-expandable' ) );
  };

  this.getExpandableTarget = function() {
    var expandable = this.getExpandableOffice();
    return expandable.element( by.css( '.o-expandable_target' ) );
  };

  this.getExpandableShowBtn = function() {
    var expandable = this.getExpandableOffice();
    return expandable.element( by.css( '.o-expandable_cue-open' ) );
  };

  this.getExpandableHideBtn = function() {
    var expandable = this.getExpandableOffice();
    return expandable.element( by.css( '.o-expandable_cue-close' ) );
  };
}

module.exports = TheBureauStructurePage;
