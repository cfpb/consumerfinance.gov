'use strict';

var _secondaryNav = element( by.css( '.o-secondary-navigation' ) );

var secondaryNav = {

  secondaryNav: _secondaryNav,

  expandableTarget:
    _secondaryNav.element( by.css( '.o-expandable_target' ) ),

  showButton:
    _secondaryNav.element( by.css( '.cf-icon-plus-round' ) ),

  hideButton:
    _secondaryNav.element( by.css( '.cf-icon-minus-round' ) )
};

module.exports = secondaryNav;
