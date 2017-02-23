$('a.popl').click(function (e) {
e.preventDefault();
var pop = $(this).attr("href");
	if($('div.modal').hasClass('open')){
			$('div.modal').hide();
			$('div.modal').removeClass('open').addClass('closed');
		}
	else {
		}	
$(pop).show();
$(pop).addClass('open');
$(pop).removeClass('closed');
});

$('a.close').click(function (e) {
e.preventDefault();
var pop = $(this).attr("href");
$(pop).hide();
$(pop).removeClass ('open');
$(pop).addClass('closed');
});

$('a.faded').click(function (e) {
e.preventDefault();
var fade = $(this).attr("href");
$(fade).fadeIn();
});