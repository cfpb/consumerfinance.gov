$(function(){

	$(".fellows-signup-form").submit(function(){
		$("#signup_btn").prop('disabled', true).val("Please wait...");
		
		$.post(fellowship_form_submit_url, $(this).serialize(), function(){
			$(".fellows-signup-form").html("<h3>Thank you!</h3> <p>We have your information and will be in touch with updates.</p>")
		});
		return false;
	});
});