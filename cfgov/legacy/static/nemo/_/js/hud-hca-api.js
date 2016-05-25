/* 	This script uses a local Django API to acquire a list of the 10 closest
	HUD Counselors by zip code. See hud_api_replace for more details on the
	API queries. -wernerc */


/*	This class represents a namespace of functions that should be exposed
	for testing purposes. */
cfpb_hud_hca = (function() {
	/*	check_zip() is an easy, useful function that takes a string and returns a valid zip code, or returns false.
	NOTE: "Valid" means 5 numeric characters, not necessarily "existant" and "actually addressable." */
	var check_zip = function(zip) {
		if ( (zip === null) || (zip === undefined) || (zip === false) ) {
			return false;
		}
		else {
			zip = zip.toString().replace(/[^0-9]+/g,"");
			zip = zip.slice(0,5);
			if (zip.length === 5) {
				return zip;
			}
			else {
				return false;
			}
		}
	}

	/*	check_data_structure() just makes sure your data has the correct structure before you start
		requesting properties that don't exist in generate_html() and update_google_map() */
	var check_hud_data = function(data) {
		if ( (data === null) || (data === 0) || (data === undefined) ) {
			return false;
		}
		else if ( data.hasOwnProperty("error") ) {
			return "error";
		}
		else if ( !(data.hasOwnProperty("counseling_agencies")) ) {
			return false;
		}
		else if ( !(data.hasOwnProperty("zip")) ) {
			return false;
		}
		else {
			return true;
		}
	}

	return {
		check_zip: check_zip,
		check_hud_data: check_hud_data
	}
}());

(function($) { // start jQuery capsule

	var gmap;
	var marker_array = [];
	var zip_marker = null;




	/*	get_url_zip() is a simple function to retrieve the zip variable from the URL */
	function get_url_zip() {
		var zip = "";
		var keyvals = window.location.href.slice(window.location.href.indexOf("?") + 1).split("&");
		$.each( keyvals , function(i, val) {
			var parts = val.split("=");
			if (parts[0] == "zip") {
				zip = parts[1];
			}
		});
		return (cfpb_hud_hca.check_zip(zip));
	}

	/*	gmap_initialize() sets options and creates the google map */
	function gmap_initialize() {
		var gmap_options = {
			center: new google.maps.LatLng(40, -80),
			zoom: 2,
			mapTypeId: google.maps.MapTypeId.ROADMAP
		};
		gmap = new google.maps.Map(document.getElementById("hud_gca_api_gmap_canvas"), gmap_options);
	}
	google.maps.event.addDomListener(window, 'load', gmap_initialize);

	/* 	generate_html_results() is a key function which generates, row-by-row, the counselor
		results. It inserts each row by cloning a hidden template row, then inserts the data into
		that newly-created row. */
	function generate_html_results(data) {
		var tdlist = $("#hud_hca_api_results_table tbody");
		tdlist.html("");

		if ( cfpb_hud_hca.check_hud_data(data) === true ) {
			// Hide the message div, show the table
			$("#hud_hca_api_message").hide();
			$("#hud_hca_api_results_table").show();

			// Iterate through each result, creating an TD and inserting the data
			var agencies = data.counseling_agencies;
			$.each(agencies, function(i, val) {
				// Clone template TR and append it
				$("#hud_hca_api_row_template tr").clone().appendTo( tdlist );

				// Define listing so we can work on the right TD
				var listing = tdlist.find("tr").last();
				var number = i + 1;
				if (number < 10) {
					number = "0" + number;
				}
				listing.attr("id", "hud-result-" + number);

				var numlist = tdlist.find(".hud_hca_api_num").last();
				var listnumber = i + 1;
				numlist.prepend(listnumber + ".");

				// Set and insert  the agency name
				var name = val.nme;
				listing.find(".hud_hca_api_counselor").html(name);

				// Set and insert the street address
				var address = val.adr1;
				var address2 = val.adr2;
				if (address2 != null) {
					if ($.trim(address2) != "") {
						address += "<br>" + address2;
					}
				}
				listing.find(".hud_hca_api_adr").html(address);

				// Set and insert city, state and zip code
				var region = val.city + ", " + val.statecd;
				region += " " + val.zipcd;
				listing.find(".hud_hca_api_region").html(region);

				// Insert distance in miles
				listing.find(".hud_hca_api_miles").html(val.distance);

				// Add link to valid web sites
				var weburl = val.weburl;
				if ( weburl != "Not available") {
					weburl = '<a href="' + weburl + '">' + weburl + '</a>';
				}
				// Insert weburl
				listing.find(".hud_hca_api_site").html(weburl);

				// Determine phone number and insert result
				var phone = val.phone1;
				listing.find(".hud_hca_api_tel").html(phone);		

				// Turn valid email addresses into links
				var email = val.email;
				if ( email != "Not available" ) {
					email = '<a href="mailto:' + email + '">' + email + '</a>';
				}
				// Insert result
				listing.find(".hud_hca_api_email").html(email);

				// Determine languages and insert result
				var languages = val.languages;
				listing.find(".hud_hca_api_lang").html(languages);		

				// Determine services and insert result
				var services = val.services;
				// Reformat services
				var serv = services.split(",");
				$.each(serv, function(i, v) {
					v = $.trim(v);
					listing.find(".hud_hca_api_serv").append('<span class="hud_hca_api_serv_item">' + v + "</span>");
				});
			});
			// Show the search results meta container.
			$("#hud_hca_api_results_info").show();
		}
		else {
			if ( cfpb_hud_hca.check_hud_data(data) == "error" ) {
				$("#hud_hca_api_message").show().html("<p>Sorry, you have entered an invalid zip code.</p>");
				$("#hud_hca_api_message").append("<p>Please enter a valid five-digit ZIP code above.</p>");
			}
			// Faulty/nonexistent data, hide the table
			$("#hud_hca_api_results_info").hide();
			$("#hud_hca_api_results_table").hide();
		}
	}

	/*	generate_google_map(data) takes the data and plots the markers, etc, on
		the google map. It's called by get_counselors_by_zip(). */

	function update_google_map(data) {
		// reset the map
		for (var i = 0; i < marker_array.length; i++ ) {
			marker_array[i].setMap(null);
		}
		marker_array = [];
		if (zip_marker != null) {
			zip_marker.setMap(null);
		}
		gmap.setZoom(2); 
		var origin = new google.maps.LatLng(40, -80); 
		gmap.setCenter(origin);

		if ( cfpb_hud_hca.check_hud_data(data) === true ) {
			var lat = data.zip.lat; 
			var lng = data.zip.lng; 
			var ziplatlng = new google.maps.LatLng(lat, lng); 
			var zoom = 10; 

			gmap.setZoom(zoom); 
			gmap.setCenter(ziplatlng);

			var bounds = new google.maps.LatLngBounds();

			zip_marker = new google.maps.Marker({
				position: ziplatlng,
				icon: {
					path: google.maps.SymbolPath.CIRCLE,
					fillColor: "#FFFFFF",
					fillOpacity: 1,
					scale: 3, 
					strokeColor: "#CC0000",
					strokeWeight: 3
				},
				zIndex: -99,
				draggable: false,
				map: gmap
			});

			$.each( data.counseling_agencies, function(i, val) {
				var position = new google.maps.LatLng(val.agc_ADDR_LATITUDE, val.agc_ADDR_LONGITUDE);
				var z = 11 - i;
				var number = i + 1;
				if ( number < 10 ) {
					number = "0" + number;
				}
				marker_array[i] = new google.maps.Marker({
					position: position,
					icon: "/wp-content/themes/cfpb_nemo/_/img/hud_gmap/agc_" + number + ".png",
					map: gmap,
					title: val.nme,
					zIndex: z
				});
				bounds.extend(position);

				google.maps.event.addListener(marker_array[i], 'click', function() {
					$(document.body).animate({'scrollTop':   $("#hud-result-" + number).offset().top }, 1000);
				});	
			});

			gmap.fitBounds(bounds);
		}
	}

	/*	get_counselors_by_zip(zip) handles the AJAX request and calls other functions
		to update the contant. It takes in a zip code and calls our local API of HUD data,
		then calls generate_html_results() to generate the results list, and
		update_google_map() to update the google map. */

	function get_counselors_by_zip(zip) {
		// if zip fails check, then clear and reset the page.
		if ( cfpb_hud_hca.check_zip(zip) === false ) {
			$("#hud_hca_api_results_info").hide();
			$("#hud_hca_api_results_table").hide();	
			generate_html_results(0);
			update_google_map(0);
		}
		else {
			var results = "";
			// Testing url
			// var qurl = "/wp-content/themes/cfpb_nemo/_/inc/hud-build-proxy.php?z=" + zip;

			// Prod url
			var qurl = "/hud-api-replace/" + zip + "/";
			var request = $.ajax({
				async: true,
				dataType: "json",
				url: qurl
			});
			request.done(function(response) {
				if (response == null) {

				}
				$("#textbox").html(response);
				generate_html_results(response);
				update_google_map(response);
			});
			request.fail(function() {
				
			});
		}
	}

	$( document ).ready(function() {
		// hide the table, the info div, and the message container
		$("#hud_hca_api_message").hide();
		$("#hud_hca_api_results_info").hide();
		$("#hud_hca_api_results_table").hide();

		// On click, perform a search
		$(".hud_hca_api_form_button").click(function(event) {
			event.preventDefault();

			var zip = $("#hud_hca_api_query").val();
			zip = cfpb_hud_hca.check_zip(zip);
			if (zip !== false) {

				$("#hud_hca_api_message").show().html("Searching...");

				$("#hud_hca_api_query").val(zip);

				// Change PDF link
				$("#generate-pdf-link").attr("href", "/save-hud-counselors-list/?zip=" + zip);

				// Perform API call and generate HTML
				get_counselors_by_zip(zip);

				$(".hud_hca_api_search_zip").html(zip);
			}
			else {
				var failzip = $("#hud_hca_api_query").val();
				var failvalid = failzip.toString().replace(/[^a-zA-Z0-9\.]+/g,"");
				$("#hud_hca_api_query").val("");
				$("#hud_hca_api_message").show().html("<p>Sorry, " + failvalid + " is not a valid zip code.</p>");
				$("#hud_hca_api_message").append("<p>Please enter a valid five-digit ZIP code above.</p>");
				get_counselors_by_zip(false);
			}
		});

		// Help IE 7/8 perform a search on enter
		$("#hud_hca_api_query").keydown(function(e) {
			if (e.which == 13) {
				// alert("You pressed enter!");
				$(".hud_hca_api_form_button").trigger("click");
				return false;
			}
		});

		// On click of the print link, open print dialog
		$(".hud_hca_api_no_js_print_text").remove();
		$(".hud_hca_api_results_print").append('<a class="hud-hca-api-print" href="#print">Print list</a>');
		$(".hud_hca_api_results_print a.hud-hca-api-print").click(function() {
			window.print();
			return false;
		});

		// Provide a fallback for HTML5 placeholder for older browsers
		$("#hud_hca_api_query", function() {
			var input = document.createElement("input");
			if(("placeholder" in input)==false) { 
				$("[placeholder]").focus(function() {
					var i = $(this);
					if(i.val() == i.attr("placeholder")) {
						i.val("").removeClass("placeholder");			
					}
				}).blur(function() {
					var i = $(this);	
					if(i.val() == "" || i.val() == i.attr("placeholder")) {
						i.addClass("placeholder").val(i.attr("placeholder"));
					}
				}).blur().parents("form").submit(function() {
					$(this).find("[placeholder]").each(function() {
						var i = $(this);
						if(i.val() == i.attr("placeholder"))
							i.val("");
					})
				});
			}
		});

		
		// Show/Hide icon toggle
		$(".show-hide-link").click(function() {
			$(".show-hide-icon").toggleClass("icon-minus-alt icon-plus-alt");
		});

		// If there is a GET value for zip, load that zip immediately.
		var getzip = get_url_zip();
		if ( getzip != "" ) {
			$("#hud_hca_api_query").val(getzip);
			$(".hud_hca_api_form_button").trigger("click");
		}

	});

})(jQuery); // end anonymous function capsule