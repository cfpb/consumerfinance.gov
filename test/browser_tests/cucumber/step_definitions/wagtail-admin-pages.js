const WagtailAdminPagesPage = require(
  '../../page_objects/wagtail-admin-pages-page.js'
);
const wagtailAdminPagesPage = new WagtailAdminPagesPage();
const { defineSupportCode } = require( 'cucumber' );

defineSupportCode( function( { Then, When } ) {

  When( /I create a Wagtail (.*) Page/, function( pageType ) {

    return wagtailAdminPagesPage.createPage( pageType );
  } );

  When( /I create a draft (.*) Page with title "(.*)"/,
    function( pageType, pageTitle ) {

      wagtailAdminPagesPage.createPage( pageType );
      wagtailAdminPagesPage.setPageTitle( pageTitle );

      return wagtailAdminPagesPage.save( );
    }
  );

  When( /I publish the page/, function() {

    return wagtailAdminPagesPage.publish();
  } );

  When( /I unpublish the page/, function() {

    return wagtailAdminPagesPage.unpublish();
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
