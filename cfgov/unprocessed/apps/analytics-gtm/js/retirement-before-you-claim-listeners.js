// Retirement - Before You Claim custom analytics file

var BYCAnalytics = (function() {
  var questionsAnswered = [],
      sliderClicks = 0,
      sliderIsActive = false,
      stepOneSubmitted = false;

  function calculateAge( month, day, year, currentDate ) {
    var now = currentDate;
    if ( currentDate instanceof Date !== true  ) {
      now = new Date();
    }
    var birthdate = new Date(year, Number(month) - 1, day);
    var age = now.getFullYear() - birthdate.getFullYear();
    var m = now.getMonth() - birthdate.getMonth();
    if ( m < 0 || ( m === 0 && now.getDate() < birthdate.getDate() ) ) {
      age--;
    }
    if ( isNaN( age ) ) {
      return false;
    }
    return age;
  }


  var delay = (function(){
    var timer = 0;
    return function(callback, ms){
      clearTimeout (timer);
      timer = setTimeout(callback, ms);
    };
  })();

  $( document ).ready( function() {

    $( '#step-one-form' ).submit( function(e) {
      e.preventDefault();
      stepOneSubmitted = true;
      var month = $( '#bd-month' ).val(),
          day = $( '#bd-day' ).val();
      dataLayer.push({
        "event": "Before You Claim Interaction",
        "action": "Get Your Estimates submit birthdate",
        "label": "Birthdate Month and Day - " + month + '/' + day
      });
    });

    $( '#step-one-form' ).submit( function(e) {
      e.preventDefault();
      var month = $( '#bd-month' ).val(),
          day = $( '#bd-day' ).val(),
          year = $( '#bd-year' ).val(),
          age = calculateAge( month, day, year );
      dataLayer.push({
        "event": "Before You Claim Interaction",
        "action": "Get Your Estimates submit age",
        "label": 'Age ' + age
      });
    });

    $( '#claim-canvas' ).on( 'mousedown', 'rect', function() {
      var age = $(this).attr( 'data-age' );
      dataLayer.push({
        "event": "Before You Claim Interaction",
        "action": "Graph Age Bar clicked",
        "label": "Age " + age
      });
    });

    $( '#claim-canvas' ).on( 'mousedown', '#graph_slider-input', function() {
      sliderIsActive = true;
      sliderClicks++;
      dataLayer.push({
        "event": "Before You Claim Interaction",
        "action": "Slider clicked",
        'label': 'Slider clicked ' + sliderClicks + ' times'
      });
    });

    $( '#claim-canvas' ).on( 'click', '.age-text', function() {
      var age = $(this).attr( 'data-age-value' );
      dataLayer.push({
        "event": "Before You Claim Interaction",
        "action": "Age Text Box clicked",
        'label': 'Age ' + age
      });
    });

    $( 'body' ).on( 'mouseup', function() {
      if ( sliderIsActive === true ) {
        var age = $('.selected-age').text();
        dataLayer.push({
          "event": "Before You Claim Interaction",
          "action": "Slider released",
          'label': 'Age ' + age
        });
        sliderIsActive = false;
      }
    });

    $( 'button.lifestyle-btn' ).click( function() {
      var $container = $(this).closest( '.lifestyle-question_container' ),
          question = $container.find( 'h3' ).text().trim(),
          value = $(this).val();
      if ( questionsAnswered.indexOf( question ) === -1 ) {
        questionsAnswered.push( question );
      }
      if ( questionsAnswered.length === 5 ) {
        dataLayer.push({
          "event": "Before You Claim Interaction",
          "action": "All Lifestyle Buttons clicked",
          'label': "All button clicks"
        });
      }
      dataLayer.push({
        "event": "Before You Claim Interaction",
        "action": "Lifestyle Button clicked",
        'label': 'Question: ' + question + ' - ' + value
      });
    });

    $( 'input[name="benefits-display"]' ).click( function() {
      if ( stepOneSubmitted ) {
        var val = $(this).val();
        dataLayer.push({
          "event": "Before You Claim Interaction",
          "action": "Benefits View clicked",
          'label': val
        });
      }
    });

    $( '#retirement-age-selector' ).change( function() {
      var val = $(this).find( 'option:selected').val();
      dataLayer.push({
        "event": "Before You Claim Interaction",
        "action": "Planned Retirement Age selected",
        'label': val
      });
    });

    $( 'button.helpful-btn' ).click( function() {
      var val = $(this).val();
      dataLayer.push({
        "event": "Before You Claim Interaction",
        "action": "Was This Page Helpful clicked",
        'label': val
      });
    });

    $( '[data-tooltip-target]' ).click( function() {
      var target = $(this).attr( 'data-tooltip-target' );
      dataLayer.push({
        "event": "Before You Claim Interaction",
        "action": "Tooltip clicked",
        'label': "Target: " + target
      });
    });
  });

})(jQuery);
