
'use strict';

let BasePage = require( './wagtail-admin-base-page.js' );
let contentMenu = require( '../shared_objects/wagtail-admin-content-menu.js' );

const PAGE_TYPES = {
  ACTIVITY_LOG:           'activitylogpage',
  BLOG:                   'blogpage',
  BROWSE:                 'browsepage',
  DOCUMENT_DETAIL:        'documentdetailpage',
  EVENT_ARCHIVE:          'eventarchivepage',
  EVENT:                  'eventpage',
  HOME:                   'homepage',
  JOB_LISTING:            'joblistingpage',
  LANDING:                'landingpage',
  LEARN:                  'learnpage',
  LEGACY_BlOG:            'legacyblogpage',
  LEGACY_NEWSROOM:        'legacynewsroompage',
  NEWSROOM_LANDING:       'newsroomlandingpage',
  NEWSROOM:               'newsroompage',
  SUBLANDING_FILTERABLE: 'sublandingfilterablepage',
  SUBLANDING:            'sublandingpage'
};

const MENUS = {
  'content': contentMenu
};

class WagtailAdminPages extends BasePage {

  constructor() {
    super();

    this.addChildPageBtn = element(
      by.css( 'btn[href="/admin/pages/1/add_subpage/"]' )
    );

    this.URL = '/admin/pages/';
  }

  createPage( pageName='landing' ) {
    let normalizedPageName = pageName
                             .toUpperCase()
                             .replace(/\s/g, '_' );
    let pageType = PAGE_TYPES[normalizedPageName];
    let page_url = `add/v1/${pageType}/1`;
    let url = this.URL + page_url;

    return this.gotoURL( url );
  }

  editPage( pageId ) {
    if ( !pageId ) {
      return Promise.resolve();
    }

    let page_url = `admin/pages/${pageId}/1/edit/`;
    let url = this.URL + page_url;

    return this.gotoURL( url );
  }

  openMenu( menuType ) {
    this.menu = MENUS[menuType];

    return this.menu && this.menu.open( menuType );
  }

  closeMenu( menuType ) {

    return this.menu && this.menu.close();
  }

  selectMenuItem( menuItem ) {

    return this.menu.selectItem( menuItem );
  }

}

WagtailAdminPages.PAGE_TYPES = PAGE_TYPES;

module.exports = WagtailAdminPages;
