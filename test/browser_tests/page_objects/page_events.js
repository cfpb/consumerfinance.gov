'use strict';

function EventsPage() {
  this.get = function() {
    browser.get( '/events/' );
  };

  this.pageTitle = function() { return browser.getTitle(); };
  this.nav = element( by.css( '.nav-secondary_list' ) );
  this.heroElem = element( by.css( '.hero' ) );
  this.hero = {
    maps:    element.all( by.css( '.hero .hero_img' ) ),
    heading: this.heroElem.element( by.css( '.summary_heading' ) ),
    date:    this.heroElem.element( by.css( '.event-meta_date' ) ),
    time:    this.heroElem.element( by.css( '.event-meta_time' ) )
  };
  this.events = element.all( by.css( '.post-preview__event' ) );
  this.eventElem = this.events.first();
  this.first = {
    map:     this.eventElem.element( by.css( '.post-summary-image img' ) ),
    heading: this.eventElem.element( by.css( '.summary_heading' ) ),
    city:    this.eventElem.element( by.css( '.event-meta_city' ) ),
    state:   this.eventElem.element( by.css( '.event-meta_state' ) ),
    date:    this.eventElem.element( by.css( '.event-meta_date' ) ),
    time:    this.eventElem.element( by.css( '.event-meta_time' ) ),
    tags:    this.eventElem.element( by.css( '.tags_list' ) )
  };
}

function ArchivePage() {
  this.get = function() {
    browser.get( '/events/archive' );
  };

  this.pageTitle = function() { return browser.getTitle(); };
  this.nav = element.all( by.css( '.nav-secondary_list a' ) );
  this.events = element.all( by.css( '.post-preview__event' ) );
  this.eventElem = this.events.first();
  this.first = {
    heading: this.eventElem.element( by.css( '.summary_heading' ) ),
    city:    this.eventElem.element( by.css( '.event-meta_city' ) ),
    state:   this.eventElem.element( by.css( '.event-meta_state' ) ),
    date:    this.eventElem.element( by.css( '.event-meta_date' ) ),
    time:    this.eventElem.element( by.css( '.event-meta_time' ) ),
    tags:    this.eventElem.element( by.css( '.tags_list' ) )
  };
}

module.exports = {
  EventsPage:  EventsPage,
  ArchivePage: ArchivePage
};
