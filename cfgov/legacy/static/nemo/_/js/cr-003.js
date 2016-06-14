
if ('onhashchange' in window) {

	function show_slide(_id, instant){
		var elm = $('#'+_id);
		var cur = $('.G_ACTIVE');

		if(!elm.length)
			return;

		cur.fadeOut(instant?0:130);
		setTimeout(function(){
			elm.fadeIn(instant?0:400);
			elm.addClass('G_ACTIVE');
		}, instant?0:140);
	}

	$(function(){

		// Remove the styling that is used for browsers
		// that do not support onhashchange.
		$('.g-container').not('.G_ACTIVE')
		.removeClass('l-separated--vertical')
		.removeClass('l-divided--top')
		.hide();

		$('.g-goto').click(function() {
			var href=$(this).attr('href').replace('#','');
			window.location.hash = href;
			return false;
		});

		// Analytics
		var prev_hash_val = location.hash;

		if (window.location.hash) {
			show_slide(window.location.hash.replace('#',''), 1);
			// If you paste a url into the browser with a hash it will jump to that hash.
			// We don't want this behavior, we want the page to behave as normal so you have
			// context from the intro.
			$('html, body').scrollTop($(window.location.hash).offset().top);
		}

		// Create event for back/forward hash tag change
		$(window).bind('hashchange', function(e){
			// Slide
			var slide_id = window.location.hash.replace('#','');
			if (!slide_id)
				slide_id = 'main';
			show_slide(slide_id);
			// Analytics
			if( prev_hash_val != location.hash ) {
				prev_hash_val = location.hash;
				_gaq.push(['_trackPageview', location.pathname + location.search + location.hash]);
			}
		});

	});

} // end if

//Does this need to be in a separate section from the above? *Confirm this JS won't break anything else on cf.gov!
//*How does this work if JavaScript is disabled in the user's browser?
$(function() {
	
//Credit & debit card radio button selections display different "Submit Complaint" wells
	$('input[name=radio-ccpp]:radio').change(function() {
		var $selected_radio = $('input[name=radio-ccpp]:radio:checked');
		var selected_id = $selected_radio.attr('id');
		$('#submit-credit-card,#submit-debit-card,#submit-prepaid-card').hide();

		if (selected_id == 'radio-credit-card') {
			$('#submit-credit-card').show();
		}
		else if (selected_id == 'radio-debit-card') {
			$('#submit-debit-card').show();
		}
		else {
			$('#submit-prepaid-card').show();
		}
	});

//Money Transfer & Virtual Currency radio button selections display different "Submit Complaint" wells
	$('input[name=radio-mtvc]:radio').change(function() {
		var $selected_radio = $('input[name=radio-mtvc]:radio:checked');
		var selected_id = $selected_radio.attr('id');
		$('#submit-money-transfer2').hide();

		if (selected_id == 'radio-virtual-currency') {
			$('#submit-money-transfer2 h2').html("We're developing a new virtual currency complaint form");
			$('#submit-money-transfer2 p').html('In the meantime, please use the money transfer complaint form to submit virtual currency complaints. Use the in-page chat if you need assistance. Then <a href="https://help.consumerfinance.gov/app/tellyourstory">share your feedback</a> about the form.');
		}
		else {
				$('#submit-money-transfer2 h2').html('Submit a money transfer complaint to the CFPB');
			$('#submit-money-transfer2 p').html('You can attach documents to your complaint, such as statements, contracts, receipts, and letters to help us better understand your issue.');
		}

		$('#submit-money-transfer2').show();
	});

//"Other service" radio button selections display different "Submit Complaint" wells/links
	$('input[name=radio-money]:radio').change(function() {
		var $selected_radio = $('input[name=radio-money]:radio:checked');
		var selected_id = $selected_radio.attr('id');
		$('#submit-money-service,#credit-repair_conditional,#debt-settlement_conditional').hide();

		//Credit repair conditional radio butons
		if (selected_id == 'radio-credit-repair') {
			$('#credit-repair_conditional').fadeIn(500);
			$('input[name=radio-money_conditional]:radio').change(function() {
				var $selected_conditional = $('input[name=radio-money_conditional]:radio:checked');
				var selected_conditional_id = $selected_conditional.attr('id');				

				if (selected_conditional_id == 'radio2-credit-report') {
					$('#submit-money-service a').attr('href', 'https://help.consumerfinance.gov/app/creditreporting/ask');
					$('#submit-money-service h2').html('Submit a credit reporting complaint to the CFPB');				
				}
				else {
					$('#submit-money-service a').attr('href', 'https://help.consumerfinance.gov/app/other/ask/p_id/3070');
					$('#submit-money-service h2').html('Submit an other financial service complaint to the CFPB');
				}

				$('#submit-money-service').show();
			});
		}
		//Debt settlement conditional radio butons
		else if (selected_id == 'radio-debt-settlement') {
			$('#debt-settlement_conditional').fadeIn(500);
			$('input[name=radio-money_conditional]:radio').change(function() {
				var $selected_conditional = $('input[name=radio-money_conditional]:radio:checked');
				var selected_conditional_id = $selected_conditional.attr('id');				

				if (selected_conditional_id == 'radio2-debt-settlement') {
					$('#submit-money-service a').attr('href', 'https://help.consumerfinance.gov/app/other/ask/p_id/3047');
					$('#submit-money-service h2').html('Submit an other financial service complaint to the CFPB');				
				}
				else {
					$('#submit-money-service a').attr('href', 'https://help.consumerfinance.gov/app/debtcollection/ask#currentPage=0');
					$('#submit-money-service h2').html('Submit a debt collection complaint to the CFPB');
				}

				$('#submit-money-service').show();
			});
		}

		else {
			$('#submit-money-service h2').html('Submit an other financial service complaint to the CFPB');
			switch (selected_id)
			{
			case "radio-check-cashing":
				$('#submit-money-service a').attr('href', 'https://help.consumerfinance.gov/app/other/ask/p_id/3071');
				break;
			case "radio-foreign-currency-exchange":
				$('#submit-money-service a').attr('href', 'https://help.consumerfinance.gov/app/other/ask/p_id/3073');
				break;
			case "radio-money-order":
				$('#submit-money-service a').attr('href', 'https://help.consumerfinance.gov/app/other/ask/p_id/3072');
				break;			
			case "radio-refund-anticipation-check":
				$('#submit-money-service a').attr('href', 'https://help.consumerfinance.gov/app/other/ask/p_id/250');
				break;
			case "radio-travelers-check":
				$('#submit-money-service a').attr('href', 'https://help.consumerfinance.gov/app/other/ask/p_id/3049');
				break;
			} //close switch
			$('#submit-money-service').show();
		} //close else 

	});

// Reset detail views on URL hash change
	$(window).on('hashchange',function(){ 
		$('input[name=radio-ccpp]:radio,input[name=radio-mtvc]:radio,input[name=radio-money]:radio,input[name=radio-money_conditional]:radio').prop('checked', false);
		$('#submit-credit-card,#submit-debit-card,#submit-prepaid-card,#submit-money-transfer2,#submit-money-service,#credit-repair_conditional,#debt-settlement_conditional').hide();
	});


});
