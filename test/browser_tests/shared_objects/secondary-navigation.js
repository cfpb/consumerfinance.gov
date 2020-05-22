const _secondaryNav = element( by.css( '.o-secondary-navigation' ) );

const secondaryNav = {

  secondaryNav: _secondaryNav,

  expandableTarget:
    _secondaryNav.element( by.css( '.o-expandable_target' ) ),

  showButton:
    _secondaryNav.element( by.css( '.cf-icon-svg' ) ),

  hideButton:
    _secondaryNav.element( by.css( '.cf-icon-svg' ) )
};

module.exports = secondaryNav;
