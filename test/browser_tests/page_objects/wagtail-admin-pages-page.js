const BasePage = require( './base-page.js' );
const contentMenu = require(
  '../shared_objects/wagtail-admin-content-menu.js'
);
const clickWhenReady = require(
  '../util/click-when-ready.js'
);
const EC = protractor.ExpectedConditions;

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
  LEGACY_BLOG:            'legacyblogpage',
  LEGACY_NEWSROOM:        'legacynewsroompage',
  NEWSROOM_LANDING:       'newsroomlandingpage',
  NEWSROOM:               'newsroompage',
  SUBLANDING_FILTERABLE:  'sublandingfilterablepage',
  SUBLANDING:             'sublandingpage'
};

const MENUS = {
  content: contentMenu
};


const titleField = element( by.css( '#id_title' ) );
const saveButton = element( by.css( '.button.action-save' ) );
const dropdownToggle = element( by.css( '.dropdown-toggle' ) );
const publishButton = element( by.css( 'button[name="action-publish"]' ) );
const unpublishButton = element( by.css( 'a[href$="/unpublish/"]' ) );
const confirmUnpublishButton = element( by.css(
  'input[value="Yes, unpublish it"]'
) );

class WagtailAdminPages extends BasePage {

  constructor() {
    super();

    this.URL = '/admin/pages/';
  }

  createPage( pageName = 'landing' ) {
    const normalizedPageName = pageName
      .toUpperCase()
      .replace( /\s/g, '_' );
    const pageType = PAGE_TYPES[normalizedPageName];

    // Add the new page as a child of page ID 3 (the site root).
    const pageUrl = `add/v1/${ pageType }/3`;

    const url = this.URL + pageUrl;

    return this.gotoURL( url );
  }

  editPage( pageId ) {
    if ( !pageId ) {
      return Promise.resolve();
    }

    const pageUrl = `admin/pages/${ pageId }/1/edit/`;
    const url = this.URL + pageUrl;

    return this.gotoURL( url );
  }

  openMenu( menuType ) {
    this.menu = MENUS[menuType];

    return this.menu && this.menu.open( menuType );
  }

  closeMenu( ) {

    return this.menu && this.menu.close();
  }

  selectMenuItem( menuItem ) {

    return this.menu.selectItem( menuItem );
  }

  setPageTitle( title ) {

    return browser.wait( EC.visibilityOf( titleField ) )
      .then( function() {

        return titleField.sendKeys( title );
      } );
  }

  save( ) {

    return clickWhenReady( saveButton );
  }

  publish( ) {
    dropdownToggle.click();

    return publishButton.click();
  }

  unpublish( ) {
    dropdownToggle.click();
    unpublishButton.click();

    return confirmUnpublishButton.click();
  }

}

WagtailAdminPages.PAGE_TYPES = PAGE_TYPES;

module.exports = WagtailAdminPages;
