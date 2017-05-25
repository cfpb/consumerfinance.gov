
'use strict';

let fullWidthTextMenu = require( './wagtail-admin-full-width-text-menu.js' );
let toggleSelector = '.toggle .stream-menu-inner';
let toggleBtn = element.all( by.css( toggleSelector ) );

let contentSelector = '#content-prependmenu .stream-menu-inner';
let _content = element
               .all( by.css( contentSelector ) )
               .first();
let EC = protractor.ExpectedConditions;

function _getStreamMenuElement( selector ) {

  return _content.element( by.css( selector ) );
}

function selectItem( componentName ) {

  function _getMenuItem( fullWidthTextMenuIsActive ) {
    let menuComponentItem;
    let normalizedComponentName = componentName
                                  .replace( /\s/g, '' )
                                  .concat( 'Btn' )
                                  .toLowerCase();
    let activeMenuItems = menuItems;

    if ( fullWidthTextMenuIsActive === true ) {
      activeMenuItems = fullWidthTextMenu.getMenuItems();
    }

    for( let key in activeMenuItems ) {
      if ( key.toLowerCase() === ( normalizedComponentName ) ) {
        menuComponentItem = activeMenuItems[key];
      }
    }

    return menuComponentItem;
  }

  function _clickMenuItem( menuItem ) {

    return  browser
            .wait( EC.elementToBeClickable( menuItem ), 500 )
            .then( menuItem.click );
  }

  return  fullWidthTextMenu.isActive()
          .then( _getMenuItem )
          .then( _clickMenuItem );
}

function open() {

  return toggleBtn.click();
}

function close() {

  return toggleBtn.click();
}

let menuItems = {

  callToActionBtn:      _getStreamMenuElement( '.action-add-block-call_to_action' ),

  contentBtn:           _getStreamMenuElement( '.action-add-block-content' ),

  contentWithAnchorBtn: _getStreamMenuElement( '.action-add-block-image_text_25_75_group' ),

  emailSignupBtn:       _getStreamMenuElement( '.action-add-block-email_signup' ),

  expandableBtn:        _getStreamMenuElement( '.action-add-block-expandable' ),

  expandableGroupBtn:   _getStreamMenuElement( '.action-add-block-expandable_group' ),

  fullWidthTextBtn:     _getStreamMenuElement( '.action-add-block-full_width_text' ),

  imageText2575Btn:     _getStreamMenuElement( '.action-add-block-image_text_25_75_group' ),

  tableBlock:           _getStreamMenuElement( '.action-add-block-table_block' ),

  videoPlayerBtn:       _getStreamMenuElement( '.action-add-block-video_player' ),

  wellBtn: 		          _getStreamMenuElement( '.action-add-block-well' )

};

let contentMenu = {
  close:      close,
  menuItems:  menuItems,
  open:       open,
  selectItem: selectItem
};

module.exports = contentMenu;
