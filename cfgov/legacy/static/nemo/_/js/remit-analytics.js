/*
 Contents
 --------
 1. Utililty functions
 2. Exit Links
 3. Tracked Links
 4. File Downloads
 5. Social Tracking
 6. Newsletter Signup Form
 7. Find and Track YouTube Videos


 */

// Add in Google Analytics tracking check wrapper
// http://ejohn.org/blog/fixing-google-analytics-for-ghostery/
var track = function(category, name, value) {
    if (window._gaq) {
        window._gaq.push(['_trackEvent', category, name, value]);
    }
}; // End Google Analytics tracking check

 // 1. Utililty functions
 // Check if URL is internal.
 $(function() {
    function isInternalHref( href ) {
        if (href.indexOf('https:') == -1 && href.indexOf('http:') == -1 && href.indexOf('//') != 0) { // There's no protocol, so it's internal
            return true;
    }
    else { // There is a protocol, so we check for our domain.
            if (href.indexOf('consumerfinance.gov') !== -1) { // It contains our domain, so it's internal.
                return true;
            }
            else { // There is a protocol and not our domain, so it's external.
                return false;
            }
        }
    }

    // Now, track stuff like this: track(category, name, value);

    $(document).ready(function() {
        // Just for testing purposes
        /*
        var a = 'http://www.consumerfinance.gov';
        var b = 'http://davidakennedy.com';
        var c = '/about';

        var testInternal = isInternalHref(a);
        console.log(testInternal); // Prints true.

        var testExit = isInternalHref(b);
        console.log(testExit); // Prints false.

        var testNoProt = isInternalHref(c);
        console.log(testNoProt); // Prints true.
        // End testing
        */

        $( 'a' ).not('.exit-link, .internal-link').each(function() { // In case our links already have the class; don't include.
            var href = $(this).attr('href');
            if ( isInternalHref( href ) ) { // Internal links get a class; not tracked in Analytics.
                $(this).addClass('internal-link');
            }
            else { // Exit links get a class; this is tracked with Analytics.
                $(this).addClass('exit-link');
            }               
        });

        // 2. Exit Links
        $('a.exit-link').on('click', function(e) {
            var linkDelay = 500;
            var link_text = $(this).text();
            var link_url = $(this).attr('href');
            // Stop the link from going anywhere
            // (it's ok we saved the href and we'll fire it later)
            e.preventDefault();
            try { track('exit link', link_text, link_url); }
            // try { track('exit link', link_text, link_url); }
            catch( error ) {}

            // Give google analytics time to do its thing before changing the page url
            // http://support.google.com/analytics/answer/1136920?hl=en
            setTimeout(function() { document.location.href = link_url; }, linkDelay);
        });

        // 3. Tracked Links
        $('a.tracked-link').on('click', function(e) {
            var linkDelay = 500;
            var link_text = $(this).text();
            var link_url = $(this).attr('href');
            // Stop the link from going anywhere
            // (it's ok we saved the href and we'll fire it later)
            e.preventDefault();
            try { track('internal links', link_text, link_url); }
            catch( error ) {}

            // Give google analytics time to do its thing before changing the page url
            // http://support.google.com/analytics/answer/1136920?hl=en
            setTimeout(function() { document.location.href = link_url; }, linkDelay);
        });
        
        // 4. File Downloads
        $('a[href$="zip"],a[href$="pdf"],a[href$="doc"],a[href$="docx"],a[href$="xls"],a[href$="xlsx"],a[href$="ppt"],a[href$="pptx"],a[href$="txt"],a[href$="csv"],a[href$="jpg"],a[href$="jpeg"],a[href$="png"],a[href$="mov"],a[href$="wma"]').on('click', function(e) {
            var linkDelay = 500;
            var link_text = $(this).text();
            var link_url = $(this).attr('href');
            // Stop the link from going anywhere
            // (it's ok we saved the href and we'll fire it later)
            e.preventDefault();
            try { track('downloads', link_text, link_url); }
            catch( error ) {}

            // Give google analytics time to do its thing before changing the page url
            // http://support.google.com/analytics/answer/1136920?hl=en
            setTimeout(function() { document.location.href = link_url; }, linkDelay);
        });

        // 5. Social Tracking
        // Links in the footer
        $('#site-footer > ul.social > a').on('click', function(e) { // Selector is a placeholder for redesign.
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

        /* Twitter follow button */
        if ( typeof twttr !== 'undefined' ) {
            twttr.ready(function ( twttr ) {
                twttr.events.bind( 'click', trackTwitterFollow );
            });
        }

        function trackTwitterFollow() {
            try { track('social', 'follow', 'twitter'); }
            catch( error ) {}
        }

        /* Facebook Like button */
        if ( typeof FB !== 'undefined' ) {
            FB.Event.subscribe( 'edge.create', trackFacebookLike );
        }

        function trackFacebookLike() {
            try { track('social', 'follow', 'facebook'); }
            catch( error ) {}
        }

        /* Social sharing buttons */
        /* Facebook */
        $('.share-facebook').on('click', function(e) { // Selector is a placeholder for redesign.
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
        $('.share-twitter').on('click', function(e) { // Selector is a placeholder for redesign.
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
        $('.share-email').on('click', function(e) { // Selector is a placeholder for redesign.
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

        /* 6. Newsletter signup form */
        $('.signup').on('click', 'button', function() {
            var zip = $(this).closest('.signup').find('questionid_10376').val();
            track('social', 'signup', 'mailing list signup');
        });
    
    }); // End document ready.
}); // End anonymous function.