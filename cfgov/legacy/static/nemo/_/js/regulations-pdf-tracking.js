(function($){

      // Below code is from countvoncount and will need to be removed
      // once sitewide analytics are set up.

      // Add in Google Analytics tracking check wrapper
      // http://ejohn.org/blog/fixing-google-analytics-for-ghostery/
      var track = function(category, name, value) {
          if (window._gaq) {
              window._gaq.push(['_trackEvent', category, name, value]);
          }
      }; // End Google Analytics tracking check

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

})(jQuery);