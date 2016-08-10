
var CFPBYouTubeAnalytics = (function() {

    var videoObjects = []; // Stores all of the videos
    var timers = []; // Stores timer objects
    var elapsedTimes = []; // Stores elapsed times
    var checkPoints = []; // Stores checkPoints for each video
    var viewingTimes = [];

    function getYouTubeVideoIdFromSrc( src ) {
        var videoId = "";
        var params = src.split('embed/')[1];
        var amp = params.indexOf('?');
        if (amp != -1) {
            videoID = params.substring(0, amp);
        }
        return videoID;
    }

    function isSrcYouTubeVideo( src ) {
        if ( src.indexOf('youtube.com/embed/') !== -1 ) {
            return true;
        }
        else {
            return false;
        }
    }

    function checkTime( videoIndex ) {
        elapsedTimes[videoIndex] += 1
        var t = elapsedTimes[videoIndex];
        var video = videoObjects[videoIndex];
        var id = video.id;

        if ( timers[videoIndex] != null) {
            // Get video position
            var videoPosition = video.player.getCurrentTime();
            // Get video duration 
            var videoDuration = video.player.getDuration(); 

            // videoPosition is rounded down, then checkPoints[] is checked for that value
            var vpos = Math.floor(videoPosition);
            var cpindex = checkPoints[videoIndex].indexOf(vpos);

            // If the videoPosition is in the array, then we'd send an event and delete it from the array
            if (  cpindex != -1 ) {
                _gaq.push(['_trackEvent', 'Videos', 'Checkpoint', video.title, vpos ]);
                // Remove entry from array to prevent an event triggering multiple times
                checkPoints[videoIndex].splice(cpindex, 1); 
            }

            // elapsed time is calculated, then elapsedTimes[] is checked for that value
            var timeElapsed = Math.floor( t / 10 );
            var teindex = viewingTimes[videoIndex].indexOf(timeElapsed);

            // If the time value is in the array, then we'd send an event and delete it from the array
            if ( teindex != -1 ) {
                _gaq.push(['_trackEvent', 'Videos', 'Duration', video.title, timeElapsed ]);
                // Remove entry from array to prevent an event triggering multiple times
                viewingTimes[videoIndex].splice(teindex, 1);
            }                
        }
        timers[videoIndex] = setTimeout(checkTime, 100, videoIndex); 
    }

    function onPlayerStateChange( event ) {
        var videoIndex = event.target.id;
        var vidTitle = videoObjects[videoIndex].title;
        if ( event.data == YT.PlayerState.PLAYING ) {
            _gaq.push(['_trackEvent', 'Videos', 'Play', vidTitle ]);
            checkTime(videoIndex); // Start the timer                    
        }
        if ( event.data == YT.PlayerState.PAUSED ) {
            _gaq.push(['_trackEvent', 'Videos', 'Pause', vidTitle ]);
            if ( elapsedTimes[videoIndex] > 0 ) {
                window.clearTimeout(timers[videoIndex]); // Stop the timer
            }
        }
        if ( event.data == YT.PlayerState.ENDED ) {
            _gaq.push(['_trackEvent', 'Videos', 'Ended', vidTitle ]);
        }
    }

    function checkInitConditions( element ) {
        var isIframe = element.is('iframe');
        var notTracked = ! (element.is('[data-is-being-tracked]'));
        var hasYouTubeSrc = isSrcYouTubeVideo( element.attr('src') );
        return ( isIframe && notTracked && hasYouTubeSrc );
    }

    function findAndTrackYouTubeVideos() {
        $('iframe').each(function( index ) {
            var video = {};
            if ( checkInitConditions( $(this) ) ) {
                var src = $(this).attr('src');
                video.id = getYouTubeVideoIdFromSrc( src );

                $.ajax({
                    dataType: 'JSON',
                    url: 'https://gdata.youtube.com/feeds/api/videos/' + video.id + '?v=2&alt=json'
                })
                .done( function( data ) {
                    video.title = data.entry.title.$t;
                });

                $(this).attr( 'data-is-being-tracked', 'true' );
                $(this).attr( 'id', video.id );

                // Create a player to attach events to
                video.player = new YT.Player( video.id, { id: index, events: { 'onStateChange': onPlayerStateChange } } );
                video.player.id = index;

                // Save the video object so the events can reference it
                if ( $.inArray( video, videoObjects === -1 ) ) {
                    videoObjects.push( video );
                }

                // Initialize values for the object
                timers[index] = null;
                elapsedTimes[index] = 0;

                // Modular tracking initializer
                if ( $(this).attr("data-checkpoints") != undefined ) {
                    // create array from string
                    checkPoints[index] = $(this).attr("data-checkpoints").split(',');

                    // map strings to integers
                    $.map(checkPoints[index], function(val,i) { 
                        checkPoints[index][i] = parseInt(val); 
                    });
                }
                if ( $(this).attr("data-viewingtimes") != undefined ) {
                    // create array from string
                    viewingTimes[index] = $(this).attr("data-viewingtimes").split(',');

                    // map strings to integers
                    $.map(viewingTimes[index], function(val,i) { 
                        viewingTimes[index][i] = parseInt(val); 
                    });
                }
            }
        });
    }






    // return functions and classes for testing
    return {
        findAndTrackYouTubeVideos: findAndTrackYouTubeVideos
    }

})(jQuery); // end cfpb_pfc_ct namespace anonymous function capsule

var YouTubeTag = document.createElement('script');

YouTubeTag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(YouTubeTag, firstScriptTag);

function onYouTubeIframeAPIReady() {
    CFPBYouTubeAnalytics.findAndTrackYouTubeVideos();
}

