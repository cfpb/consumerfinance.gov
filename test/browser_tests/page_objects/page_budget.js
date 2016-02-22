'use strict';

var _getQAElement = require( '../util/qa-element' ).get;

function Budget() {

  this.get = function() {
    browser.get( '/budget/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.mainTitle = element( by.css( '.media_body h1' ) );

  this.missionSummary = _getQAElement( 'mission-summary' );

  this.missionStatements =
  _getQAElement( 'mission-statements', true ).all( by.css( 'li' ) );

  this.budgetSections =
  _getQAElement( 'budget-section', true ).all( by.css( '.content-l_col' ) );

  this.budgetSectionTitles = this.budgetSections.all( by.css( 'h2' ) );

  this.budgetSectionDescriptions = _getQAElement( 'budget-section-desc', true );

  this.budgetSectionLinks = this.budgetSections.all( by.css( 'a' ) );

  this.businessWithCFPBSection = _getQAElement( 'business-with-CFPB-section' );

  this.businessWithCFPBTitle =
  this.businessWithCFPBSection.element( by.css( '.header-slug_inner' ) );

  this.businessWithCFPBDescription =
    _getQAElement( by.css( 'business-with-CFPB-desc' ) );

  this.businessWithCFPBLink =
  this.businessWithCFPBSection.element( by.css( 'a' ) );

  this.relatedLinksTitle =
  element( by.css( '.related-links .header-slug_inner' ) );

  this.relatedLinks = element.all( by.css( '.related-links a' ) );

}

module.exports = Budget;
