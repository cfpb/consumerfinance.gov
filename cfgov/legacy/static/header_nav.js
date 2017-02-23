$(document).ready(function() {
  $("#main_nav a").click(function(e) {
	e.preventDefault();
	var target = $($(this).attr("href"));
	$("#main_nav li").removeClass("activeLink");
	if(target.hasClass("activeNav")) {
	  target.removeClass("activeNav");
	  $("#main_header").animate({paddingBottom: 0}, 200, function() {$("#containment div").css("z-index",10);});
	}
	else {
	  $("#containment div").removeClass("activeNav");
	  $(this).parent().addClass("activeLink");
	  target.addClass("activeNav");
	  $("#containment div").css("z-index",10);
	  target.css("z-index",30);
	  $("#main_header").animate({paddingBottom: target.outerHeight()}, "fast");
	}
  });
  $(".infield input").keyup(function() {
	  if ($(this).val()) {
		$(this).addClass("filled");
	  }
	  else {
		$(this).removeClass("filled");
	  }
	});
	$(".infield textarea").keyup(function() {
	  if ($(this).val()) {
		$(this).addClass("filled");
	  }
	  else {
		$(this).removeClass("filled");
	  }
	});
});