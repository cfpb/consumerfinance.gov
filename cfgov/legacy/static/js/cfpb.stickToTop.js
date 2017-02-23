var stickyElement, lock, topOffset, leftOffset;

(function($) {
	$.stickToTop = function(element, options) {
		this.options = {};
		element.data('stickToTop', this);
		this.init = function(element, options) {
			this.options = $.extend({}, $.fn.stickToTop.defaultOptions, options);
			stickyElement = element;
			lock = $(element).offset().top - this.options.distance;
			topOffset = this.options.distance + 'px';
			leftOffset = $(element).offset().left;
			$(window).scroll(checkPosition);
		  	$(window).resize(checkPosition);
		  	$(window).on("load",checkPosition);
		};

		this.init(element, options);
	};

	$.fn.stickToTop = function(options) {
		return this.each(function() {
			(new $.stickToTop($(this),options));
		});
	}

	function checkPosition() {
		footerOffset = $('#footer').offset().top - parseFloat($('#footer').css('padding-top')) - parseFloat($('#footer').css('border-top-width')) - parseFloat($('#footer').css('margin-top'));
        haveReachedFooter = $(window).scrollTop() + $(stickyElement).height() >= footerOffset - 2

		if($(window).scrollTop() > lock && !haveReachedFooter) {
			$(stickyElement).css({'position' : 'fixed', 'top' : topOffset, 'left' : leftOffset});
		}
        else if ($(window).scrollTop() > lock && haveReachedFooter){
            absoluteTop = footerOffset - $(stickyElement).height() - parseFloat($(stickyElement).css('padding-bottom'));
			$(stickyElement).css({'position' : 'absolute', 'top' : absoluteTop, 'left' : leftOffset});
        }
		else {
			$(stickyElement).css({'position' : '', 'top' : '', 'left' : ''});
		}
	};

	$.fn.stickToTop.defaultOptions = {
		distance: 15
	}


})(jQuery);
