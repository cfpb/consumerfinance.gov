'use strict';

const WagtailAdminPagesPage = require(
  '../../page_objects/wagtail-admin-pages-page.js'
);
const wagtailAdminPagesPage = new WagtailAdminPagesPage();
const { defineSupportCode } = require( 'cucumber' );
const { expect } = require( 'chai' );

defineSupportCode( function( { Then, When } ) {

  When( /I create a Wagtail (.*) Page/, function( pageType ) {
    wagtailAdminPagesPage.createPage( pageType );

    return browser.getCurrentUrl()
           .then( function( url ) {
             expect( url ).to.contain( pageType.toLowerCase() );
           } );
  } );

  Then( /I open the (.*) menu/, function( menuType ) {

    return wagtailAdminPagesPage.openMenu( menuType );
  } );

  Then( /I select the (.*) (?: atom|molecule|organism|element)/,
    function( component ) {

      return wagtailAdminPagesPage.selectMenuItem( component );
    }
  );

} );
