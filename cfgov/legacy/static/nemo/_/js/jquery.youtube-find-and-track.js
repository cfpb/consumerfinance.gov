(function($)
{

    /**
     * ========================================================================
     * Find and Track YouTube Videos
     * Find YouTube videos on a page and track them with google analytics
     * ========================================================================
     * cfpb.github.com: @davidakennedy, @mikem
     *
     * YouTube Iframe API Documentation
     * https://developers.google.com/youtube/iframe_api_reference
     * 
     * Code adapted from:
     * - http://www.lunametrics.com/blog/2012/10/22/automatically-track-youtube-videos-events-google-analytics/
     * - http://lunametrics.wpengine.netdna-cdn.com/js/lunametrics-youtube.js
     * Code adapted by Alex Mueller for ISITE Design http://isitedesign.com
     */

    $.fn.findAndTrackYouTubeVideos = function( ) {

        var videoObjects = [], // Stores all of the videos
            // Simple variable to track if the event was captured once,
            // we had a problem with events firing more than once in firefox
            // and during scrubbing so this is a temporary stopgap.
            wasTriggeredOnce = {
                playing: false,
                ended: false
            };

        function onPlayerStateChange( event ) {
            var videoIndex = event.target.id - 1;
            if ( event.data == YT.PlayerState.PLAYING && wasTriggeredOnce.playing === false ) {
                 wasTriggeredOnce.playing = true;
                try { _gaq.push(['_trackEvent', 'Videos', 'Play', videoObjects[videoIndex].title ]); }
                catch( error ) {}
            // } else if ( event.data == YT.PlayerState.PAUSED ) {
            //     try { _gaq.push(['_trackEvent', 'Videos', 'Pause', videoObjects[videoIndex].title ]); }
            //     catch( error ) {}
            } else if ( event.data == YT.PlayerState.ENDED && wasTriggeredOnce.ended === false ) {
                 wasTriggeredOnce.ended = true;
                try { _gaq.push(['_trackEvent', 'Videos', 'Ended', videoObjects[videoIndex].title ]); }
                catch( error ) {}
            }
        }

        function isSrcYouTubeVideo( src ) {
            if ( src.indexOf('youtube.com/embed/') !== -1 ) {
                return true;
            } else {
                return false;
            }
        }

        function getYouTubeVideoIdFromSrc( src ) {
            var videoId;
            // The ID comes after '/embed/'
            if ( src.substr( 0,29 ) == 'http://www.youtube.com/embed/' ) {
                videoId = src.substr( 29 );
            } else if ( src.substr( 0,30 ) == 'https://www.youtube.com/embed/' ) {
                videoId = src.substr( 30 );
            }
            // If the ID ends with extra characters remove them
            if ( videoId.indexOf('?') > -1 ) {
                videoId = videoId.substr( 0, videoId.indexOf('?') );
            }
            return videoId;
        }

        function checkInitConditions( e ) {
            var $e = $( e ),
                isIframe = $e.is('iframe'),
                notAlreadyTracked = !$e.is('[data-is-findAndTrackYouTubeVideos]'),
                hasYouTubeSrc = isSrcYouTubeVideo( $e.attr('src') );
            return ( isIframe && notAlreadyTracked && hasYouTubeSrc );
        }

        // Loop through each object to see if it meets our init conditions. If
        // it does then save the info we need for tracking and attach tracking
        // events.
        if ( $.fn.findAndTrackYouTubeVideos.isIframeApiReady ) {
            return this.each(function() {
                var $iframe = $( this ),
                    video = {};
                // Grab the video info we'll need to track it
                if ( checkInitConditions( $iframe ) ) {
                    video.id = getYouTubeVideoIdFromSrc( $iframe.attr('src') );
                    // Saving the title is trickier we need to pull it from the
                    // YouTube data API
                    $.ajax({
                        dataType: 'JSON',
                        url: 'https://gdata.youtube.com/feeds/api/videos/' + video.id + '?v=2&alt=json'
                    })
                    .done( function( data ) {
                        video.title = data.entry.title.$t;
                    });
                    // Flag this element so we know we're tracking it
                    $iframe.attr( 'data-is-findAndTrackYouTubeVideos', '' );
                    // Put the video ID on the iframe as its id attribute
                    $iframe.attr( 'id', video.id );
                    // Create a player to attach events to
                    video.player = new YT.Player( video.id, { events: { 'onStateChange': onPlayerStateChange } } );
                    // Save the video object so the events can reference it
                    if ( $.inArray( video, videoObjects === -1 ) ) {
                        videoObjects.push( video );
                    }
                }
            });
        } else {
            return false;
        }
    };

    $.fn.findAndTrackYouTubeVideos.isIframeApiReady = false;

}(jQuery));

/**
 * ============================================================================
 * YouTube API Functions
 * Keep this stuff in the global namespace
 * ============================================================================
 */

var tag = document.createElement('script');
tag.src = "//www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// This function gets called by the YouTube Iframe API
function onYouTubeIframeAPIReady() {
    // We're only calling the plugin when the YouTube Iframe API is ready
    // because we need it to create YouTube player objects for tracking.
    $.fn.findAndTrackYouTubeVideos.isIframeApiReady = true;
    $('iframe').findAndTrackYouTubeVideos();
}

