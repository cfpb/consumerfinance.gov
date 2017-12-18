const pageChooser = require(
  '../../shared_objects/wagtail-admin-link-chooser.js'
);

const { defineSupportCode } = require( 'cucumber' );

defineSupportCode( function( { When } ) {

  When( /I enter (.*) in the page chooser search field/, function( text ) {

    return pageChooser.enterSearchText( text );
  } );

  When( /I select the link titled (.*)/, function( linkTitle ) {

    return pageChooser.selectPageLink( linkTitle );
  } );

} );
