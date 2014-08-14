/**
 * cf-expandables
 * https://github.com/cfpb/cf-expandables
 *
 * A public domain work of the Consumer Financial Protection Bureau
 */

(function( $ ) {

  $.fn.expandable = function( userSettings ) {

    return $( this ).each(function() {

      var settings = $.extend({
            expandOnFocus: false
          }, userSettings ),
          $this = $( this ),
          $target = $this.find('.expandable_target'),
          $content = $this.find('.expandable_content');

      $target.attr( 'aria-controls', $content.attr('id') );

      if ( $this.hasClass('expandable__expanded') ) {
        $content.css( 'display', 'block' );
        $content.attr( 'aria-expanded', 'true' );
        $target.attr( 'aria-pressed', 'true' );
      } else {
        $content.css( 'display', 'none' );
        $content.attr( 'aria-expanded', 'false' );
        $target.attr( 'aria-pressed', 'false' );
      }

      $target.on( 'click', function( ev ) {

        var duration;
        ev.preventDefault();
        ev.stopPropagation();

        if ( $target.attr('aria-pressed') === 'true' ) {
          $content.attr( 'aria-expanded', 'false' );
          $target.attr( 'aria-pressed', 'false' );
          duration = $.fn.expandable.calculateCollapseDuration( $content.height() );
        } else {
          $content.attr( 'aria-expanded', 'true' );
          $target.attr( 'aria-pressed', 'true' );
          duration = $.fn.expandable.calculateExpandDuration( $content.height() );
        }

        $this.toggleClass('expandable__expanded');
        $content.slideToggle({
          duration: duration,
          easing: 'easeOutExpo'
        });

      });

    });

  };

  $.fn.expandable.calculateExpandDuration = function( height ) {
    return $.fn.expandable.constrainValue( 450, 900, height * 4 );
  };

  $.fn.expandable.calculateCollapseDuration = function( height ) {
    return $.fn.expandable.constrainValue( 350, 900, height * 2 );
  };

  $.fn.expandable.constrainValue = function( min, max, duration ) {
    if ( duration > max ) {
        return max;
    } else if ( duration < min ) {
        return min;
    } else {
        return duration;
    }
  };

  // Auto init
  $('.expandable').expandable();

}(jQuery));