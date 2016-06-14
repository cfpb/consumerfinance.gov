/* ==========================================================================
   Babel Event tracking for Google Analytics, using jQuery
   @todo create reusable function for links that change the page
   ========================================================================== */

$(function() {

    // http://stackoverflow.com/questions/1335851/what-does-use-strict-do-in-javascript-and-what-is-the-reasoning-behind-it
    'use strict';

    // The amount of time to delay a url change after a link is clicked
    var cfpbDomain = 'consumerfinance.gov',
        linkDelay = 500;


    /* ==========================================================================
       !!!!!!!!!!!!!!!!!!!!!!!!!!!! Debug overrides !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
       ========================================================================== */

    // @todo figure out a way for this debug info to be used with the social widget
    // code at the bottom of this file

    // // Convert google analytics events to a simple console.log
    // var _gaq = {};
    // _gaq.push = function() {
    //     console.log(arguments[0]);
    // };

    // // Prevent setTimeout() from changing document.location.href
    // var setTimeout = function() {
    //     return false;
    // };

    // // For local testing of relative consumerfinance.gov links
    // cfpbDomain = 'http://127.0.0.1:8000/';

    /* ==========================================================================
       !!!!!!!!!!!!!!!!!!!!!!!!!!!! END - Debug overrides !!!!!!!!!!!!!!!!!!!!!!!
       ========================================================================== */


    /* ==========================================================================
       Utility functions
       ========================================================================== */

    function isHrefCFPB( e, lang ) {

        var isCFPB = false,
            isLang = false;

        // Check if this link is cfpb
        if ( e.href.indexOf( cfpbDomain ) !== -1 ) {
            isCFPB = true;
        }

        // Check for the language test
        if ( lang === undefined ) {

            // If we're not checking for language only return isCFPB
            return isCFPB;

        } else {

            // Do the language test
            if ( e.hreflang === lang ) {
                isLang = true;
            }
            return isCFPB && isLang;

        }

    }


    /* ==========================================================================
       Banner Links, any link inside of .wrapper-banner
       ========================================================================== */

    $('.wrapper-banner a').click(function( e ) {

        // Save the href so we can change the url with js
        var $this = $( this ),
            link_url = $this.attr('href');

        // Stop the link from going anywhere
        // (it's ok we saved the href and we'll fire it later)
        e.preventDefault();

        // Use a try statement in case there are google analytics errors
        // that could prevent the rest of this code from changing the url
        // thus breaking the link completely instead of delaying it!
        if ( $this.is('.english-link') ) {

            // English link
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'English site button', 'Header']); }
            catch( error ) {}

        }

        // Give google analytics time to do its thing before changing the page url
        // http://support.google.com/analytics/answer/1136920?hl=en
        setTimeout(function() { document.location.href = link_url; }, linkDelay);

    });


    /* ==========================================================================
       Header Links, any link inside of .wrapper-header
       Exceptions:
       - Complaint phone number (which is tracked further down the script)
       ========================================================================== */

    // Define the selectors for this area
    var headerTargets = new AnalyticsTarget({
        containers: [ '.wrapper-header' ],
        targets: [ 'a[href]' ],
        exceptions: [ 'a[href^="tel:"]' ]
    });

    $( headerTargets.selectContainers() )
    .delegate( headerTargets.selectTargetsForDelegate(), 'click', function( e ) {

        // Save the href so we can change the url with js
        var $this = $( this ),
            link_url = $this.attr('href');

        // Stop the link from going anywhere
        // (it's ok we saved the href and we'll fire it later)
        e.preventDefault();

        // Use a try statement in case there are google analytics errors
        // that could prevent the rest of this code from changing the url
        // thus breaking the link completely instead of delaying it!
        if ( $this.is('.main-nav a') ) {

            // Main nav and policy link
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'Header links', link_url]); }
            catch( error ) {}

        } else if ( $this.is('.brand-logo') ) {

            // Logo
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'Logo', link_url]); }
            catch( error ) {}

        }

        // Give google analytics time to do its thing before changing the page url
        // http://support.google.com/analytics/answer/1136920?hl=en
        setTimeout(function() { document.location.href = link_url; }, linkDelay);

    });


    /* ==========================================================================
       Body Links, any link inside of .wrapper-body
       Exceptions:
       - Complaint phone number (which is tracked further down the script)
       - .js-videoreplace links (because we're tracking the play state of the video)
       ========================================================================== */

    // Define the selectors for this area
    var bodyTargets = new AnalyticsTarget({
        containers: [ '.wrapper-body' ],
        targets: [ 'a[href]' ],
        exceptions: [
            '.js-videoreplace',
            'a[href^="tel:"]'
        ]
    });

    $( bodyTargets.selectContainers() )
    .delegate( bodyTargets.selectTargetsForDelegate(), 'click', function( e ) { 

        // Save the href so we can change the url with js
        var $this = $( this ),
            link_url = $this.attr('href');

        // Stop the link from going anywhere
        // (it's ok we saved the href and we'll fire it later)
        e.preventDefault();

        // Use a try statement in case there are google analytics errors
        // that could prevent the rest of this code from changing the url
        // thus breaking the link completely instead of delaying it!

        if ( isHrefCFPB( this, 'en-US' ) ) {

            // English site links
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'English site button', link_url]); }
            catch( error ) {}

        } else if ( $this.is('.share-facebook') ) {

            try { _gaq.push(['_trackEvent', 'Social', 'Share', 'facebook']); }
            catch( error ) {}

        } else if ( $this.is('.share-twitter') ) {

            try { _gaq.push(['_trackEvent', 'Social', 'Share', 'twitter']); }
            catch( error ) {}

        } else if ( $this.is('.share-email') ) {

            try { _gaq.push(['_trackEvent', 'Social', 'Share', 'email']); }
            catch( error ) {}

        } else if ( $this.is('.share .print') ) {

            // Print button in share bar
            try { _gaq.push(['_trackEvent', 'Social', 'Print', link_url]); }
            catch( error ) {}

        } else if ( $this.is('.ac-catnav-heading a') ) {

            // Category links on ask cfpb landing page
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'Category links', link_url]); }
            catch( error ) {}

        } else if ( $this.is('.ac-catnav-list a') ) {

            // Answer links on ask cfpb landing page
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'Answer links', link_url]); }
            catch( error ) {}

        } else if ( $this.is('a.ac-catnav-learn') ) {

            // Learn more links on ask cfpb landing page
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'Learn more links', link_url]); }
            catch( error ) {}

        } else if ( $this.is('.pagination-filter, .ac-filters a') ) {

            // Filter links on ask cfpb
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'Filters', link_url]); }
            catch( error ) {}

        } else if ( $this.is('.ac-related-topics a') ) {

            // Related topic links on ask cfpb
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'Related topic links', link_url]); }
            catch( error ) {}

        } else if ( $this.is('.ac-similar-answers a') ) {

            // Similar answer links on ask cfpb
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'Similar answer links', link_url]); }
            catch( error ) {}

        } else if ( $this.is('.page-parent .catnav a') && !$this.is('.btn, [class^="btn-"]') ) {

            // Answers category links on the homepage
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'Get answer links', link_url]); }
            catch( error ) {}

        } else if ( $this.is('.hero a') ) {

            // Hero links
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'Hero links', link_url]); }
            catch( error ) {}

        } else if ( $this.is('.btn, [class^="btn-"]') ) {

            // Generic button tracking
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'Button links', link_url]); }
            catch( error ) {}

        } else {

            // Generic link tracking
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'Body links', link_url]); }
            catch( error ) {}

        }

        // Give google analytics time to do its thing before changing the page url
        // http://support.google.com/analytics/answer/1136920?hl=en
        setTimeout(function() { document.location.href = link_url; }, linkDelay);

    });

    /* Body Buttons, all <button> or form elements in .wrapper-body
       ========================================================================== */

    $('.wrapper-body button, .wrapper-body input[type="submit"]').click(function( e ) {

        var $this = $( this );

        // Use a try statement in case there are google analytics errors
        // that could prevent the rest of this code from changing the url
        // thus breaking the link completely instead of delaying it!
        if ( $this.is('.ac-disclaimer button') ) {

            // Answer disclaimer on ask cfpb answer pages
            var $toggledContent = $('.ac-disclaimer .js-showtoggle-content');

            if ( $toggledContent.attr( 'data-state' ) === 'open' ) {

                try { _gaq.push(['_trackEvent', 'Page Interactions', 'About these answers', 'Open']); }
                catch( error ) {}

            } else if ( $toggledContent.attr( 'data-state' ) === 'closed' ) {

                try { _gaq.push(['_trackEvent', 'Page Interactions', 'About these answers', 'Close']); }
                catch( error ) {}

            }

        } else if ( $this.is('#js-ac-qrating-helpful input[type="submit"]') ) {

            // Clicks "Yes" on ask cfpb answer poll
            try { _gaq.push(['_trackEvent', 'Answer Ratings', 'Yes']); }
            catch( error ) {}

        } else if ( $this.is('#js-ac-qrating-helpful .js-showtoggle-trigger') ) {

            // Clicks "No" on ask cfpb answer poll
            try { _gaq.push(['_trackEvent', 'Answer Ratings', 'No']); }
            catch( error ) {}

        } else if ( $this.is('#js-ac-qrating-not-helpful input[type="submit"]') ) {

            // Clicks "Submit" on ask cfpb answer poll

            // Save all the checked checkbox values as an array
            var reasonForNo = [];

            // Loop through the checkboxes and if they are checked take the value
            // and replace spaces with underscores, then add it to the reasonForNo array
            $('#js-ac-qrating-not-helpful ul input').each(function() {
                var $self = $(this),
                    $label = $( 'label[for="' + $self.attr('id')+ '"]');
                if ( $self.is(':checked') ) {
                    reasonForNo.push( $label.text().split(' ').join('_') );
                }
            });

            // If there were any checked checkboxes merge the text from its
            // corresponding label into a string and send it to google analytics;
            // if there weren't then just send a plain submit event
            if ( reasonForNo.length > 0 ) {
                reasonForNo = reasonForNo.join(',');
                try { _gaq.push(['_trackEvent', 'Answer Ratings', 'Submit your feedback', 'reason:' + reasonForNo]); }
                catch( error ) {}
            } else {
                try { _gaq.push(['_trackEvent', 'Answer Ratings', 'Submit your feedback']); }
                catch( error ) {}
            }

        } else if ( $this.is('#js-ac-qrating-not-helpful .js-showtoggle-trigger') ) {

            // Clicks "Cancel" on ask cfpb answer poll
            try { _gaq.push(['_trackEvent', 'Answer Ratings', 'Cancel']); }
            catch( error ) {}

        }

    });


    /* ==========================================================================
       Footer Links, any link inside of .wrapper-footer
       ========================================================================== */

    $('.wrapper-footer a').click(function( e ) {

        // Save the href so we can change the url with js
        var $this = $( this ),
            link_url = $this.attr('href');

        // Stop the link from going anywhere
        // (it's ok we saved the href and we'll fire it later)
        e.preventDefault();

        // Use a try statement in case there are google analytics errors
        // that could prevent the rest of this code from changing the url
        // thus breaking the link completely instead of delaying it!
        if ( $this.is('.main-nav a, .policy a') ) {

            // Main nav and policy link
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'Footer links', link_url]); }
            catch( error ) {}

        } else if ( $this.is('.english-link') ) {

            // English site link
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'English site button', 'Footer']); }
            catch( error ) {}

        } else if ( $this.is('.social-nav a') ) {

            // Social links
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'Footer links', link_url]); }
            catch( error ) {}

        }

        // Give google analytics time to do its thing before changing the page url
        // http://support.google.com/analytics/answer/1136920?hl=en
        setTimeout(function() { document.location.href = link_url; }, linkDelay);

    });


    /* ==========================================================================
       Complaint phone number
       ========================================================================== */

    $('a[href="tel:+18554112372"]').click(function() {

        // Strip parentheses for ga
        var phone_number = $(this).text().replace( /\(|\)/g, '');

        try { _gaq.push(['_trackEvent', 'Page Interactions', 'Complaint phone number', phone_number]); }
        catch( error ) {}

    });

});

/* ==========================================================================
   Third Party Social Widgets
   ========================================================================== */

/* Twitter follow button
   ========================================================================== */

if ( typeof twttr !== 'undefined' ) {
    twttr.ready(function ( twttr ) {
        twttr.events.bind( 'click', trackTwitterFollow );
    });
}

function trackTwitterFollow() {
    try { _gaq.push(['_trackEvent', 'Social', 'Follow', 'twitter']); }
    catch( error ) {}
}

/* FB Like button
   ========================================================================== */

if ( typeof FB !== 'undefined' ) {
    FB.Event.subscribe( 'edge.create', trackFacebookLike );
} else {
    setTimeout(function() {
        if ( typeof FB !== 'undefined' ) {
            FB.Event.subscribe( 'edge.create', trackFacebookLike );
        }
    }, 2000);
}

function trackFacebookLike() {
    try { _gaq.push(['_trackEvent', 'Social', 'Follow', 'facebook']); }
    catch( error ) {}
}

/* ==========================================================================
   Utility functions
   http://stackoverflow.com/questions/470832/getting-an-absolute-url-from-a-relative-one-ie6-issue
   ========================================================================== */

function escapeHTML(s) {
    return s.split('&').join('&amp;').split('<').join('&lt;').split('"').join('&quot;');
}

function qualifyURL(url) {
    var el= document.createElement('div');
    el.innerHTML= '<a href="'+escapeHTML(url)+'">x</a>';
    return el.firstChild.href;
}
