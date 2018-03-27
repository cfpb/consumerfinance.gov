// Owning a Home - Loan Estimate custom analytics file

var OAHLEAnalytics = (function() {

  var delay = (function(){
    var timer = 0;
    return function(callback, ms){
      clearTimeout (timer);
      timer = setTimeout(callback, ms);
    };
  })();

  jQuery( '.tab-link' ).click( function() {
    var text = jQuery( this ).text().trim();
    dataLayer.push({
      "event": 'OAH Loan Estimate Interaction',
      "action": 'Tab click',
      "label": text
    });
  });

  jQuery( '.form-explainer_page-link ' ).click( function() {
    var pageNumber = 'Page ' + jQuery( this ).attr('data-page');
    dataLayer.push({
      "event": 'OAH Loan Estimate Interaction',
      "action": 'Page link click',
      "label": pageNumber
    });
  });

  jQuery( '.form-explainer_page-buttons button' ).click( function() {
    var currentPage = 'Page ' + jQuery( '.form-explainer_page-link.current-page' ).attr('data-page'),
        action = 'Next Page button clicked';
    if ( jQuery(this).hasClass( 'prev' ) ) {
      action = 'Previous Page button clicked';
    }
    dataLayer.push({
      "event": 'OAH Loan Estimate Interaction',
      "action": action,
      "label": currentPage
     });

  });

  jQuery( '.expandable_target' ).click( function() {
    var ele = jQuery(this),
        tab = ele.closest( '.explain' ).find( '.active-tab' ),
        tabText = tab.find( '.tab-label' ).text().trim();
    delay(
      function() {
        var state = ele.attr( 'aria-pressed' ),
            action = "Expandable collapsed - " + tabText,
            label = jQuery( '<p>' + ele.find('.expandable_label').html() + '</p>' ),
            text = '';

        label.find('span').empty();
        text = label.text().trim();

        if ( state === 'true' ) {
          action = "Expandable expanded - " + tabText;
        }
        dataLayer.push({
          "event": 'OAH Loan Estimate Interaction',
          "action": action,
          "label": text
        });
    }, 250 );
  });

  jQuery( '.image-map_overlay' ).click( function() {
    var href = jQuery(this).attr( 'href' ),
        text = jQuery(this).text().trim();
    delay(
      function() {
        var action = "Image Overlay click - expandable collapsed",
            target = jQuery( href );
        if ( target.hasClass( 'expandable__expanded' ) ) {
          action = "Image Overlay click - expandable expanded";
        }
        dataLayer.push({
          "event": 'OAH Loan Estimate Interaction',
          "action": action,
          "label": text
        });
      }, 250 );
  });



})(jQuery);
