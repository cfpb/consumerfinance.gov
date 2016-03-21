'use strict';

var stayInformedSection = require( '../shared_objects/stay-informed-section' );
var rssSection = require( '../shared_objects/rss-section' );
var _getQAElement = require( '../util/qa-element' ).get;

function PressResources() {

  Object.assign( this, stayInformedSection, rssSection );

  this.get = function() {
    browser.get( '/newsroom/press-resources/' );
  };

  this.pageTitle = browser.getTitle;

  this.mainTitle = _getQAElement( 'main-title' );

  this.subTitle = element( by.css( '.press-contacts_title' ) );

  this.sideNav = element( by.css( '.o-secondary-navigation' ) );

  this.contactList = element( by.css( '.press-contacts_main-contact-list' ) );

  this.contactListEmail = element.all(
  by.css( '.press-contacts_main-contact-list .list_link' ) ).get( 0 );

  this.contactListPhone = element.all(
  by.css( '.press-contacts_main-contact-list .list_link' ) ).get( 1 );

  this.contactPersons =
  element.all( by.css( '.press-contacts_people .contact-person' ) );

  this.pressSectionTitle = element( by.css( '.press-photos-bios_title' ) );

  this.pressSectionIntro = element( by.css( '.press-section_intro' ) );

  this.directorsBio =
  element.all( by.css( '.press-photos-bios .contact-person' ) ).get( 0 );

  this.directorsImage =
  this.directorsBio.all( by.css( '.contact-person_photo' ) ).get( 0 );

  this.directorsName =
  this.directorsBio.all( by.css( '.contact-person_name' ) ).get( 0 );

  this.directorsBioLink =
  this.directorsBio.all( by.css( '.list__links .list__link' ) ).get( 0 );

  this.directorsHighResImageLink =
  this.directorsBio.all( by.css( '.list__links .list_link' ) ).get( 1 );

  this.directorsLowResImageLink =
  this.directorsBio.all( by.css( '.list__links .list_link' ) ).get( 2 );

  this.deputyDirectorBio =
  element.all( by.css( '.press-photos-bios .contact-person' ) ).get( 1 );

  this.deputyDirectorsName =
  this.deputyDirectorBio.all( by.css( '.contact-person_name' ) ).get( 0 );

  this.deputyDirectorsImage =
  this.deputyDirectorBio.all( by.css( '.contact-person_photo' ) ).get( 0 );

  this.deputyDirectorsHighResImageLink =
  this.deputyDirectorBio.all( by.css( '.list__links .list_link' ) ).get( 0 );

  this.deputyDirectorsLowResImageLink =
  this.deputyDirectorBio.all( by.css( '.list__links .list_link' ) ).get( 1 );

}

module.exports = PressResources;
