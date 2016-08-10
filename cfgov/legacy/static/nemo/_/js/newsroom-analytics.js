(function($) {
    // Add in Google Analytics tracking check wrapper
    var track = function(category, name, value) {
        'use strict';
        if (window._gaq) {
            window._gaq.push(['_trackEvent', category, name, value]);
        }
    }; // End Google Analytics tracking check
    $( document ).ready(function() {
        
        // Code for logging tagged Topics & Types -wernerc
        var toptypes = ''; // string for event value
        var ttarray = []; // array for storing values

        // Add "Topics" to the array
        $( '.SelectedTag' ).each( function(index)  {
            if ( $( this ).is( ':checked' ) ) {
                if (toptypes != '') toptypes = toptypes + ',';
                ttarray.push( $( this ).val() );
            }
        });

        // Add "Types" to the array
        $( '.SelectedCategory' ).each( function(index)  {
            if ( $( this ).is( ':checked' ) ) {
                if (toptypes != '') toptypes = toptypes + ',';
                ttarray.push( $( this ).val() );
            }
        });
        ttarray.sort(); // Alphabetize the array so that events are consistent.
        $.each(ttarray, function(index, value) { // Craft the string
            if (toptypes != '') toptypes += ',';
            toptypes += value;
        });

        // gaq.push the event content
        track('topics_and_types', toptypes);

        /* Social sharing buttons and subscriptions */
        /* Facebook */
        $('.share-facebook').on('click', function(e) {
            var linkDelay = 500;
            var link_url = $(this).attr('href');
            // Stop the link from going anywhere
            // (it's ok we saved the href and we'll fire it later)
            e.preventDefault();
            try { track('social', 'share', 'facebook'); }
            catch( error ) {}

            // Give google analytics time to do its thing before changing the page url
            // http://support.google.com/analytics/answer/1136920?hl=en
            setTimeout(function() { document.location.href = link_url; }, linkDelay);
        });

        /* Twitter */
        $('.share-twitter').on('click', function(e) {
            var linkDelay = 500;
            var link_url = $(this).attr('href');
            // Stop the link from going anywhere
            // (it's ok we saved the href and we'll fire it later)
            e.preventDefault();
            try { track('social', 'share', 'twitter'); }
            catch( error ) {}

            // Give google analytics time to do its thing before changing the page url
            // http://support.google.com/analytics/answer/1136920?hl=en
            setTimeout(function() { document.location.href = link_url; }, linkDelay);
        });

        /* Email */
        $('.share-email').on('click', function(e) {
            var linkDelay = 500;
            var link_url = $(this).attr('href');
            // Stop the link from going anywhere
            // (it's ok we saved the href and we'll fire it later)
            e.preventDefault();
            try { track('social', 'share', 'email'); }
            catch( error ) {}

            // Give google analytics time to do its thing before changing the page url
            // http://support.google.com/analytics/answer/1136920?hl=en
            setTimeout(function() { document.location.href = link_url; }, linkDelay);
        });

        /* Track social media profile views */
        $('.stay-connected').on('click', function(e) {
            var linkDelay = 500;
            var link_text = $(this).text();
            var link_url = $(this).attr('href');
            // Stop the link from going anywhere
            // (it's ok we saved the href and we'll fire it later)
            e.preventDefault();
            try { track('social', link_text, link_url); }
            catch( error ) {}

            // Give google analytics time to do its thing before changing the page url
            // http://support.google.com/analytics/answer/1136920?hl=en
            setTimeout(function() { document.location.href = link_url; }, linkDelay);
        });

        /* Subscriptions */
        /* RSS link */
        $('.rss-link').on('click', function(e) {
            var linkDelay = 500;
            var link_text = $(this).text();
            var link_url = $(this).attr('href');
            // Stop the link from going anywhere
            // (it's ok we saved the href and we'll fire it later)
            e.preventDefault();
            try { track('subscriptions', 'rss', link_text); }
            catch( error ) {}

            // Give google analytics time to do its thing before changing the page url
            // http://support.google.com/analytics/answer/1136920?hl=en
            setTimeout(function() { document.location.href = link_url; }, linkDelay);
        });

        /* Email: right sidebar */
        $('.signup-link').on('click', function(e) {
            track('subscriptions', 'email signup', 'right sidebar');
        });

        /* Image links */
        $('.images-link').on('click', function(e) {
            var linkDelay = 500;
            var link_url = $(this).attr('href');
            // Stop the link from going anywhere
            // (it's ok we saved the href and we'll fire it later)
            e.preventDefault();
            try { track('images link', 'images link', link_url); }
            catch( error ) {}

            // Give google analytics time to do its thing before changing the page url
            // http://support.google.com/analytics/answer/1136920?hl=en
            setTimeout(function() { document.location.href = link_url; }, linkDelay);
        });
    });
}(jQuery));