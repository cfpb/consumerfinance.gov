// Google Analytics for /mortgage/

$(function() {
    // Track file downloads 
    $('a[href$="zip"],a[href$="pdf"],a[href$="doc"],a[href$="docx"],a[href$="xls"],a[href$="xlsx"],a[href$="ppt"],a[href$="pptx"],a[href$="txt"],a[href$="csv"]').click(function() {
        var link_text = $(this).text();
        var link_url = $(this).attr('href');
        try {
            _gaq.push(['_trackEvent','Mortgage Downloads', link_text, link_url]);
        }
        catch( error ) {}
        // Delay for _gaq.push() to complete
        setTimeout(function() {
            document.location.href = link_url;
        }, 500);
    });
    
    // Track link clicks
    $('#maincontent a').click(function(e) {
        e.preventDefault();
        var link_text = $(this).text();
        var link_url = $(this).attr('href');
        try {
            _gaq.push(['_trackEvent', 'Mortgage Link Clicked', link_text, link_url]);
        }
        catch( error ) {}
        // if a link starts with '#' then no delay is necessary
        if ( link_url.substring(0,1) == '#' ) {
            document.location.href = link_url;            
        }
        else {
            // Delay for _gaq.push() to complete
            setTimeout(function() {
                document.location.href = link_url;
            }, 500);
        }
    });
});
