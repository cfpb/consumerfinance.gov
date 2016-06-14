/* ==========================================================================
   jQuery plugins
   ========================================================================== */

(function($)
{

    /*
     * ======================================================================
     * cfpbVideoReplace
     * ======================================================================
     *
     * Replaces content with youtube embed code
     *
     * DEPENDANCIES:
     * - jquery.fitvids.js
     *
     * Simply link to the youtube video with a normal link, if js is disabled
     * the link will work as normal.
     *
     * If js is enabled youtube embed code will be created using the href of
     * the link and the selector's html content will be replaced.
     *
     * Usage:
     *
     * <a href="http://youtu.be/xX3fhgEwyVA">Play</a>
     *
     * $('a[href^="http://youtu.be"]').cfpbVideoReplace();
     * 
     */

    $.fn.cfpbVideoReplace = function( ) {

        return this.each(function() {

            var $this = $( this );

            $this.addClass('js-videoreplace');

            function replaceWithVideo( e ) {

                var videoLink = $this.attr('href'),
                    videoId = '',
                    $newThis;

                // Get the video id
                // http://stackoverflow.com/questions/10591547/how-to-get-youtube-video-id-from-url
                videoId = videoLink.match(/(?:https?:\/{2})?(?:w{3}\.)?youtu(?:be)?\.(?:com|be)(?:\/watch\?v=|\/)([^\s&]+)/);

                // Stop the link from going anywhere
                e.preventDefault();

                // If the id is valid insert the embed code
                if ( videoId !== null ) {

                    // Replace $this (a link) with $newThis (not a link)
                    $newThis = $this.contents();
                    $this.replaceWith( $newThis );

                    // Insert the embed code and call the fitvids plugin
                    // to allow for flexible video
                    $newThis
                    .html(
                        '<iframe width="820" height="461" src="http://www.youtube.com/embed/' +
                        videoId[1] +
                        '?autoplay=1&rel=0&showinfo=0&theme=light" frameborder="0" allowfullscreen></iframe>'
                    )
                    .fitVids();

                    // Call video tracking code
                    if ( typeof $.fn.findAndTrackYouTubeVideos !== 'undefined' ) {
                        $('iframe').findAndTrackYouTubeVideos();
                    }
                }
            }

            // Initiate the video replacement via click
            $this.click( replaceWithVideo );

        });
    };

    /*
     * ======================================================================
     * cfpbInputFilledCheck
     * ======================================================================
     *
     * Adds a class if the user has typed something into the field,
     * removes the class if it is empty
     * 
     * Usage: $('input').cfpbInputFilledCheck();
     * 
     * You can specify the class added:
     * $('input').cfpbInputFilledCheck({ 'className': 'has-stuff' });
     * 
     */

    $.fn.cfpbInputFilledCheck = function( userSettings ) {

        return this.each(function() {

            var $this = $( this ),
                settings = $.extend({ 'className': 's-filled' }, userSettings );

            // Add a class to hide the label if the user has typed in the input
            $this.keyup(function() {
                if ( $this.val() ) {
                  $this.addClass( settings.className );
                } else {
                  $this.removeClass( settings.className );
                }
            });

        });
    };

    /*
     * ======================================================================
     * cfpbSimpleFormPost
     * ======================================================================
     *
     * Simple form posting using $.post
     * 
     * Usage: $('#form').cfpbSimpleFormPost();
     * 
     * Supports two activity message types [ waiting, results ]
     * --------------------------------------------------------
     * If you need activity messages add them yourself to the dom using either
     * the default selectors or your own. This plugin will show and hide them
     * for you. Data returned from the post will be added to resultsTarget if
     * you added one.
     * 
     * Settings
     * ----------------------------------------------------------------------
     * You can change some settings when you initialize the plugin:
     * 
     * speed:          the animation speed (a number(ms) or string 'slow')
     * waitingTarget:  a selector specifying an element to use as a waiting message
     * resultsTarget:  a selector specifying an element to use as a results message
     * 
     */

    $.fn.cfpbSimpleFormPost = function( userSettings ) {

        return this.each(function() {

            var $form = $( this ),
                defaultSettings = {
                    'speed':                500,
                    'easing':               'easeOutExpo',
                    'waitingTarget':        '.js-simpleform-waiting',
                    'resultsTarget':        '.js-simpleform-results'
                },
                settings = $.extend( defaultSettings, userSettings ),
                url = $form.attr('action'),
                vals,
                $waitingTarget = $( settings.waitingTarget ),
                $resultsTarget = $( settings.resultsTarget );

            // Make sure activity messages are initially hidden
            $waitingTarget.hide();
            $resultsTarget.hide();

            // When a submit button is clicked send the form data
            $form.submit( submitForm );

            function submitForm( event ) {

                // Stop form from submitting so we can do that with ajax
                event.preventDefault();

                // Get the form values
                vals = $form.serialize();

                // Hide the form and show the waiting message
                $form.slideUp( settings.speed, settings.easing );
                $waitingTarget.slideDown( settings.speed );

                // Send the form values and show results when done
                $.post( url, vals ).done( showResults );
            }

            function showResults( data ) {

                // Hide the waiting message,
                // Show the results message
                $waitingTarget.slideUp( settings.speed, settings.easing );
                $resultsTarget.slideDown( settings.speed, settings.easing );

                // If any data came back add it
                // to the results message
                //$resultsTarget.html( data );
            }

        });
    };

    /*
     * ======================================================================
     * cfpbShowToggle
     * ======================================================================
     *
     * Show/hide toggle pattern supporting sliding and fading
     * 
     * Usage: $('.js-showtoggle-toggle').cfpbShowToggle();
     * 
     * Settings
     * ----------------------------------------------------------------------
     * You can change some of the settings when you initialize the plugin:
     * 
     * triggerTarget:  a selector that triggers the toggle
     * contentTarget:  a selector that represents the content to toggle
     * startOpen:      a class name, if it is present on contentTarget it will
     *                 initially be open instead of hidden
     * animation:      animation type ('slide' or 'fade')
     * speed:          the animation speed (a number(ms) or string 'slow')
     * 
     * Example:
     * $('.fade-toggle').cfpbShowToggle({
     *   'triggerTarget': '#toggle-trigger',
     *   'contentTarget': '#toggle-content',
     *   'startOpen': '#toggle-content',
     *   'animation': 'fade',
     *   'speed': 10000,
     * });
     * 
     */

    $.fn.cfpbShowToggle = function( userSettings ) {

        return this.each(function() {

            var defaultSettings = {
                    'animation': 'slide', // options: slide, fade
                    'speed': 500,
                    'easing': 'easeOutExpo',
                    'styleHookClass': 'collapsible',
                    'startOpen': 'js-showtoggle-content-open',
                    'triggerTarget': '.js-showtoggle-trigger',
                    'contentTarget': '.js-showtoggle-content'
                },
                settings = $.extend( defaultSettings, userSettings ),
                $this = $( this ),
                $trigger,
                $content;

            function init() {
                // Find the required child elements
                $trigger = $this.find( settings.triggerTarget );
                $content = $this.find( settings.contentTarget );
                // Proceed only if we have the two required elements
                if ( $trigger.length > 0 && $content.length > 0 ) {
                    // This is a marker to let the plugin know that it has
                    // already been initialized on this element.
                    $this.attr( 'data-is-cfpbShowToggle', '' );
                    // On click toggle the content
                    $trigger.click( toggle );
                    // Hide the content classes unless specified otherwise
                    $content.each(function(){
                        var $self = $( this );
                        // Add a styling hook by adding a customizeable class
                        $self.addClass( settings.styleHookClass );
                        // Set the initial visibility, as well as the state attribute
                        if ( !$self.hasClass( settings.startOpen ) ) {
                            $self.hide();
                            $self.attr( 'data-state', 'closed' );
                        } else {
                            $self.attr( 'data-state', 'open' );
                        }
                    });
                }
            }

            function toggle( event ) {
                // Stop the toggle trigger from triggering native events
                event.preventDefault();
                // Update the data-state attribute with the current state
                updateContentStates();
                // Toggle the content with an animation defaulting
                // to slide if no custom animation was set
                if ( settings.animation === 'fade' ) {
                    $content.fadeToggle( settings.speed, settings.easing );
                } else {
                    $content.slideToggle( settings.speed, settings.easing );
                }
            }

            function updateContentStates() {
                // Update the data-state attribute with the current state.
                // We can use this as a hook for things like capturing custom
                // events in google analytics to see if the user opened/closed it.
                $content.each(function( ){
                    var $self = $( this );
                    if ( $self.attr( 'data-state') === 'open' ) {
                        $self.attr( 'data-state', 'closed' );
                    } else {
                        $self.attr( 'data-state', 'open' );
                    }
                });
            }

            // Initiate the plugin but prevent it from initiating twice on the
            // same element. We know if it was already set by checking for the
            // data-is-cfpbShowToggle attribute which gets set in init().
            if ( !$this.is('[data-is-cfpbShowToggle]') ) {
                init();                
            }

        });
    };

}(jQuery));
