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
       Banner Links
       [!] Currently limited to only the spanish link, we should update
           `.wrapper-banner a.espanol-link` to `.wrapper-banner a` when we're ready
           to track all links in the banner
       ========================================================================== */

    $('.wrapper-banner a.espanol-link').click(function( e ) {

        // Save the href so we can change the url with js
        var $this = $( this ),
            link_url = $this.attr('href');

        // Stop the link from going anywhere
        // (it's ok we saved the href and we'll fire it later)
        e.preventDefault();

        // Use a try statement in case there are google analytics errors
        // that could prevent the rest of this code from changing the url
        // thus breaking the link completely instead of delaying it!
        if ( $this.is('.espanol-link') ) {

            // English link
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'Spanish site button', 'Header']); }
            catch( error ) {}

        }

        // Give google analytics time to do its thing before changing the page url
        // http://support.google.com/analytics/answer/1136920?hl=en
        setTimeout(function() { document.location.href = link_url; }, linkDelay);

    });


    /* ==========================================================================
       Footer Links, any link inside of .wrapper-footer
       [!] Currently limited to only the spanish link, we should update
           `#footer a.espanol-link` to `#footer a` when we're ready
           to track all links in the banner
       ========================================================================== */

    $('#footer a.espanol-link').click(function( e ) {

        // Save the href so we can change the url with js
        var $this = $( this ),
            link_url = $this.attr('href');

        // Stop the link from going anywhere
        // (it's ok we saved the href and we'll fire it later)
        e.preventDefault();

        // Use a try statement in case there are google analytics errors
        // that could prevent the rest of this code from changing the url
        // thus breaking the link completely instead of delaying it!
        if ( $this.is('.espanol-link') ) {

            // English site link
            try { _gaq.push(['_trackEvent', 'Page Interactions', 'Spanish site button', 'Footer']); }
            catch( error ) {}

        }

        // Give google analytics time to do its thing before changing the page url
        // http://support.google.com/analytics/answer/1136920?hl=en
        setTimeout(function() { document.location.href = link_url; }, linkDelay);

    });

});