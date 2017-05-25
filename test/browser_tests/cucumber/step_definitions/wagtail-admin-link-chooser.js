
'use strict';

var pageChooser = require( '../../shared_objects/wagtail-admin-link-chooser.js' );

var {defineSupportCode} = require( 'cucumber' );
var {expect} = require( 'chai' );

defineSupportCode( function( { Then, When } ) {

  When( /I enter (.*) in the page chooser search field/, function ( text ) {

    return pageChooser.enterSearchText( text );
  } );

  When( /I select the link titled (.*)/, function ( linkTitle ) {

    return pageChooser.selectPageLink( linkTitle );
  } );

} );
