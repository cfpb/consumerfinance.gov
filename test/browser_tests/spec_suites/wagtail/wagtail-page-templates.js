'use strict';

var LandingPage = require( '../../page_objects/page_wagtail_templates.js' ).landing;
var SubLandingPage = require( '../../page_objects/page_wagtail_templates.js' ).sublanding;
var BrowsePage = require( '../../page_objects/page_wagtail_templates.js' ).browse;
var BrowseFilterablePage = require( '../../page_objects/page_wagtail_templates.js' ).browse_filterable;
var SublandingFilterablePage = require( '../../page_objects/page_wagtail_templates.js' ).sublanding_filterable;
var EventArchivePage = require( '../../page_objects/page_wagtail_templates.js' ).event_archive;
var LearnPage = require( '../../page_objects/page_wagtail_templates.js' ).learn;
var EventPage = require( '../../page_objects/page_wagtail_templates.js' ).event;
var DocumentDetailPage = require( '../../page_objects/page_wagtail_templates.js' ).docdetail;

describe('Wagtail Landing Page', function () {
    var page;

    beforeAll(function () {
        page = new LandingPage();
        page.get();
    });

    it('should properly load in a browser',
        function () {
            expect(page.pageTitle()).toContain('Landing Page | Consumer Financial Protection Bureau');
        }
    );

});

describe('Wagtail SubLanding Page', function () {
    var page;

    beforeAll(function () {
        page = new SubLandingPage();
        page.get();
    });

    it('should properly load in a browser',
        function () {
            expect(page.pageTitle()).toContain('Sublanding Page | Consumer Financial Protection Bureau');
        }
    );

});

describe('Wagtail Browse Page', function () {
    var page;

    beforeAll(function () {
        page = new BrowsePage();
        page.get();
    });

    it('should properly load in a browser',
        function () {
            expect(page.pageTitle()).toContain('Browse Page | Consumer Financial Protection Bureau');
        }
    );

});

describe('Wagtail Browse Filterable Page', function () {
    var page;

    beforeAll(function () {
        page = new BrowseFilterablePage();
        page.get();
    });

    it('should properly load in a browser',
        function () {
            expect(page.pageTitle()).toContain('Browse Filterable Page | Consumer Financial Protection Bureau');
        }
    );

});

describe('Wagtail Sublanding Filterable Page', function () {
    var page;

    beforeAll(function () {
        page = new SublandingFilterablePage();
        page.get();
    });

    it('should properly load in a browser',
        function () {
            expect(page.pageTitle()).toContain('Sublanding Filterable Page | Consumer Financial Protection Bureau');
        }
    );

});

describe('Wagtail Event Archive Page', function () {
    var page;

    beforeAll(function () {
        page = new EventArchivePage();
        page.get();
    });

    it('should properly load in a browser',
        function () {
            expect(page.pageTitle()).toContain('Event Archive Page | Consumer Financial Protection Bureau');
        }
    );

});

describe('Wagtail Learn Page', function () {
    var page;

    beforeAll(function () {
        page = new LearnPage();
        page.get();
    });

    it('should properly load in a browser',
        function () {
            expect(page.pageTitle()).toContain('Learn Page | Consumer Financial Protection Bureau');
        }
    );

});

describe('Wagtail Event Page', function () {
    var page;

    beforeAll(function () {
        page = new EventPage();
        page.get();
    });

    it('should properly load in a browser',
        function () {
            expect(page.pageTitle()).toContain('Event Page | Consumer Financial Protection Bureau');
        }
    );

});

describe('Wagtail Document Detail Page', function () {
    var page;

    beforeAll(function () {
        page = new DocumentDetailPage();
        page.get();
    });

    it('should properly load in a browser',
        function () {
            expect(page.pageTitle()).toContain('Document Detail Page | Consumer Financial Protection Bureau');
        }
    );

});