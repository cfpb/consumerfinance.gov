var linkElement, hidemenu, dropdown, dropping;



function escHandler(e) {
    if(e.keyCode == 27) {
        window.clearTimeout(countdown);
        var target = $("#interScreen p:first a").attr("href");
        $("#interScreen").remove();
        $('a[href="'+target+'"]').get(0).focus();
        $("body").unbind("keydown",escHandler);
        return false;
    }
    return true;
}

function dropMenu() {
    dropping = 1;
    $("#closeMenu").remove();
    var menuItem = $(linkElement);
    var target = menuItem.attr("href");
    if ( target != "/" ) {
        var position = menuItem.offset().left - 1;
        $(target).css("left",position + "px");
        var position = menuItem.offset().top + menuItem.outerHeight();
        $(target).css("top",position + "px");
        $(target).append("<a id='closeMenu' class='close' href='#'>close menu</a>");
        $("a#closeMenu").click(function(e) {
            e.preventDefault();
            var myParent = $(this).parent().attr("id");
            hideMenu();
            $('a[href="#'+myParent+'"]').removeClass("active");
            $('a[href="#'+myParent+'"]').get(0).focus();
            $('a[href="#'+myParent+'"]').css("outline","none");
        });
        var height = $(target).show().height();
        $(target).hide().css('height', 0);
        $(target).show().animate({height: height}, 400, function() {
            dropping = 0;
        });
        $(target+" a:first").get(0).focus();
        $(target+" a:first").css("outline","none");
        menuItem.addClass("active");
        dropdown = 0;
    }
}

function hideMenu() {
    $(".active").removeClass("active");
    $("#closeMenu").remove();
    $("#subnav nav").slideUp();
}

function resizeOembed() {
  var newWidth = $('article').width();
  var newHeight = newWidth/16*9;
  $('body.post article iframe').attr('width', newWidth);
  $('body.post article iframe').attr('height', newHeight);
}
$(document).ready(resizeOembed());

/* trigger when page is ready */
$(document).ready(function (){
    $("#header nav a").mouseenter(function() {
        window.clearTimeout(hidemenu);
        var target = $(this).attr("href");


        if ( (target == "/") || ($(target).css("display") == "none") ) {
            hideMenu();
            linkElement = this;
            dropdown = window.setTimeout(dropMenu, 500);
        }

        return false;
    }).mouseleave(function() {
        hidemenu = window.setTimeout(hideMenu, 500);
        window.clearTimeout(dropdown);
        dropdown = 0;
    }).click(function(e) {
        var clicked = $(this);
        var target = clicked.attr("href");
        if(target == "/") {
            return true;
        }
        if(dropping) {
            return false;
        }
        if ( $(target).css("display") == "none") {
            if(!dropdown && !dropping) {
                hideMenu();
                linkElement = this;
                dropMenu();
            }
        }
        else {
            if(!dropping) {
                hideMenu();
            }
        }
        return false;
    });
    $("#subnav nav").mouseenter(function() {
        window.clearTimeout(hidemenu);
        window.clearTimeout(dropdown);
        var hovering = "#" + $(this).attr("id");
    }).mouseleave(function() {
        var hovering = "";
        hidemenu = window.setTimeout(hideMenu,500);
    });
    $(".inf input").keyup(function() {
      if ($(this).val()) {
        $(this).addClass("filled");
      }
      else {
        $(this).removeClass("filled");
      }
    });
    $(".inf textarea").keyup(function() {
      if ($(this).val()) {
        $(this).addClass("filled");
      }
      else {
        $(this).removeClass("filled");
      }
    });
    $(".signup").submit(function() {
        var form = $(this);     form.children("fieldset").children("p:last-child").children("button").attr("disabled","disabled");
        $.ajax({
            type: "POST",
            url: $(this).attr("action"),
            data: form.serialize(),
            complete: function(req, status_msg) {
                if(status_msg){
                    form.children("fieldset").hide();
                    var thanks;
                    if(form.attr("data-thanks")) {
                        thanks = form.attr("data-thanks");
                    }
                    else {
                        thanks = "Thanks, we’ll be in touch.";
                    }
                    form.append("<p>"+thanks+"</p>");
                } else {
                    form.children("fieldset").hide();
                    form.append("<p>Something went wrong. Please try again later.</p>");
                }
            }
        });
        return false;
    });
    $("a > img").each(function() {
        $(this).parent().addClass("noStyles");
    });
    $(".mini a").mouseup(function(){
        var link = $(this).attr("href");
        link = link.replace("http://","/");
        link = link.replace("http://","/");
        var tracker = "/v/topshare"+link;
        _gaq.push(['_trackPageview',tracker]); });
    $(".botshare a").mouseup(function(){
        var link = $(this).attr("href");
        link = link.replace("http://","/");
        link = link.replace("http://","/");
        var tracker = "/v/botshare"+link;
        _gaq.push(['_trackPageview',tracker]);
    });
    $('iframe').each(function() {
        var url = $(this).attr("src")
        if ( url.indexOf('youtube') !== -1 ) {
            var char = "?";
            if ( url.indexOf("?") !== -1 ) {
                char = "&";
            }
            $(this).attr("src",url+char+"wmode=transparent");
        }
    });
    $('a[href$="pdf"]').each(function() {
        $(this).addClass("pdf");
    });
});


/* SEARCH BOX */
$(function(){

    // on page-load, determin the right placeholder color
    var searchLabelNd = $('#search_form label');
    if($('#search_form #query').val())
        searchLabelNd.fadeOut(50);
    else
        searchLabelNd.fadeIn(50);


    // placeholder text Behavior on focus and blur
    $('#search_form #query').focus(function(){
        if($(this).val())
            searchLabelNd.fadeOut(50);
        else
            searchLabelNd.fadeIn(50);
    });

    $('#search_form #query').keyup(function(){
        if($('#search_form #query').val())
            searchLabelNd.fadeOut(50);
        else
            searchLabelNd.fadeIn(50);
    });

    $('#search_form #query').blur(function(){
        if($(this).val() == ''){
            searchLabelNd.fadeIn(50);
        }else{
            searchLabelNd.fadeOut(50);
        }
    });

});

/* END SEARCH BOX */


/* ********* */
/* ACCORDION */
/* ********* */

(function( $ ) {
  $.fn.cAccordion = function() {
  // display the currently active '.active' panel, hide all others. (All panels are shown if JS is off)
  this.find(".accordion-group > div").hide().filter(".active > div").show();

  // 508 compliance - adding show or hide text on every link
  this.find(".accordion-group").each(function(i, accgrp) {
    var $accgrp = $(accgrp),
    text = "Show";
    if ($accgrp.hasClass('active')) {
      text = "Hide";
    }
    $accgrp.find('h3 a').prepend($("<span />").html(text));
  });

  this.find(".accordion-group h3").click(function(e){
    e.preventDefault();

    var $accordion_h3 = $(this),
    $accordion_group = $accordion_h3.parent(),
    $accordion_panel = $accordion_group.find('> div'),
    $accordian = $accordion_group.parent(),
    already_active = false;
    already_active = $accordion_group.hasClass('active'); //returns true
    //console.log(already_active);

    //Update the show/hide text for the accordion group clicked
    if (already_active) {
      $accordion_group.find("span").html("Show");
    }
    else {
      $accordion_group.find("span").html("Hide");
    }

    // if the accordion does not all show all
    if ($accordian.hasClass('show-one')) {
      // you must collapse any other open panel before opening the one clicked
      $accordian.find('.accordion-group.active > div').slideUp();
      $accordian.find('.accordion-group.active').removeClass('active');
      $accordian.find('.accordion-group.active span').html("Show");
      // if the panel being click was already open, close it
      if (already_active) {
        $accordion_group.removeClass('active');
        return;
      }

    }

    $accordion_group.toggleClass("active");
    //Only call $.slideToggle() to open or close the content if it is not currently being animated:
    $accordion_panel.not(":animated").slideToggle();

  });

  };

  // auto-init
  $(function(){
  $('.accordion').cAccordion();
  });

})( jQuery );


/* ********* */
/* SHOW-HIDE */
/* ********* */

(function( $ ) {
  $.fn.cShowHide = function() {

  this.filter(".default-hidden").find(".show-hide-content").hide();

  this.find(".show-hide-link").click(function(e) {

    e.preventDefault();
    var $clicked_show_hide_a = $(this);
    // The entire SHow/Hide DOM object:
    var $show_hide = $(this).parent(".show-hide");


    var $show_hide_content = $show_hide.find("> .show-hide-content");
    //console.log($_show_hide_content)

    var textshow = $(this).attr('data-textshow');
    //console.log('_textshow: ' + _textshow);
    var texthide = $(this).attr('data-texthide');
    //console.log('_texthide: ' + _texthide);

    if($show_hide.hasClass("default-hidden")) {
      $show_hide.removeClass("default-hidden");
      $show_hide_content.slideDown(500);
      $clicked_show_hide_a.find("span").html(texthide);
    }
    else {
      $show_hide.addClass("default-hidden");
      $show_hide_content.slideUp(500);
      $clicked_show_hide_a.find("span").html(textshow);
    }
  });
  };

  // auto-init
  $(function(){
  $('.show-hide').cShowHide();
  });

})( jQuery );


/* ********* */
/* END SHOW-HIDE */
/* ********* */

/* ********* */
/* TABSET */
/* ********* */


(function( $ ) {
  $.fn.cTab = function() {

  var $tabset = this;

  // Hide all the inactive tabs. They are not hidden by CSS for 508 compliance
  $tabset.find(".tabcontent > div").hide().filter(".active").show();

  // Attach a click handler to all tab anchor elements
  $tabset.find(".tabs a").click(function(e) {
    e.preventDefault();

    // The clicked <a> tag is this
    var $this = $(this),
    $this_tabset = $this.closest(".tabset"),
    this_tabname = $this.attr('data-tabname'),
    $this_tabcontent = $this_tabset.find('.tabcontent [data-tabname=' + this_tabname + ']');

    // make everything inactive
    $this_tabset.find('.tabcontent .active').hide();
    $this_tabset.find('.active').removeClass('active');

    // make clicked active
    $this_tabcontent.addClass("active").show();
    $this.addClass("active");
  });
  };

  // auto-init
  $(function(){
  $('.tabset').cTab();
  });

})( jQuery );

/* ********* */
/* END TABSET */
/* ********* */

/* ********** */
/* Sticky nav */
/* ********** */

/*!
 * jQuery Scrollspy Plugin
 * Author: @sxalexander
 * Licensed under the MIT license
 * https://github.com/sxalexander/jquery-scrollspy
 */
(function(e,t,n,r){e.fn.extend({scrollspy:function(n){var r={min:0,max:0,mode:"vertical",buffer:0,container:t,onEnter:n.onEnter?n.onEnter:[],onLeave:n.onLeave?n.onLeave:[],onTick:n.onTick?n.onTick:[]};var n=e.extend({},r,n);return this.each(function(t){var r=this;var i=n;var s=e(i.container);var o=i.mode;var u=i.buffer;var a=leaves=0;var f=false;s.bind("scroll",function(t){var n={top:e(this).scrollTop(),left:e(this).scrollLeft()};var l=o=="vertical"?n.top+u:n.left+u;var c=i.max;var h=i.min;if(e.isFunction(i.max)){c=i.max()}if(e.isFunction(i.min)){h=i.min()}if(c==0){c=o=="vertical"?s.height():s.outerWidth()+e(r).outerWidth()}if(l>=h&&l<=c){if(!f){f=true;a++;e(r).trigger("scrollEnter",{position:n});if(e.isFunction(i.onEnter)){i.onEnter(r,n)}}e(r).trigger("scrollTick",{position:n,inside:f,enters:a,leaves:leaves});if(e.isFunction(i.onTick)){i.onTick(r,n,f,a,leaves)}}else{if(f){f=false;leaves++;e(r).trigger("scrollLeave",{position:n,leaves:leaves});if(e.isFunction(i.onLeave)){i.onLeave(r,n)}}}})})}})})(jQuery,window)

/* end plug-in */

/* Report specific js for sticky nav */
$(document).ready(function() {
  $(window).scroll(function() {
      $('.report header h2').each(function(){
          var scrtop = $(window).scrollTop();
          var positioner = $(this).parent().parent();
          var offset = positioner.offset();
          offset.bottom = positioner.height() + offset.top;
          var id = positioner.attr('id');
          section_link = $('#nav-list').find('a[href="#'+id+'"]');
          if ((offset.top <= scrtop) && (offset.bottom > scrtop)) {
              section_link.css("color", "#010101");
          }
          else {
              section_link.css("color", "");
          }
      });
    });
  if($('.report nav').length > 0) {
    $('.report nav').scrollspy({
      min: $('.report nav').offset().top,
      max: $('#footer').offset().top + 5000,
      onEnter: function(element, position) {
        $(".report nav").addClass('fixed');
      },
      onLeave: function(element, position) {
        $(".report nav").removeClass('fixed');
      }
    });
  }
});

/* Stripe table rows in older browsers */
// if jquery is running and IE > 9
      if (typeof $ !== 'undefined' && typeof is_lt_IE9 !== 'undefined') {
        $(document).ready(function() {
          $('table tbody tr:even').addClass('even');
          $('table tbody tr:odd').addClass('odd');
        });
      }
/* End Stripe table rows in older browsers */

/* Start Newsroom */

// For Filteing between tags and categories

jQuery(function($) {
      $('#Newsroom input.SelectedTag, #Newsroom input.SelectedCategory, #Newsroom input.selectedtag').change(function() {
       var s =  window.location.href ;
        var type = "";
        var topic = "";

       $('input[type=checkbox]').each(function () {
          var sThisVal = (this.checked ? "1" : "0");
          if (this.checked)
          {
           if (this.className == 'SelectedCategory')
           {
          type =  type + $(this).val() + ",";
           }
           else
          {
            topic = topic +  $(this).val() + "+";
          }
          }
        });

       var url = "/newsroom/";
      function add_param_to_url(url, param){
        if(url[url.length-1] == '/')
          return url + '?' + param;
        else
          return url + '&' + param;
      }
      if(type)
        url = add_param_to_url(url, "type=" + type.replace(/,$/, ''));
      if(topic)
        url = add_param_to_url(url, "topic=" + topic.replace(/\+$/, ''));

      window.location.href = url;

      });

      });



// Accordion for Monthly archive

      function cfpbAccordion(openFirst) {


        if(openFirst === true){
          // Select all the divs that are descendants of the show-hide div and hide all that are not first
          $(".accordion div:not(:first)").addClass("close");


          //So the slideToggle will animate the close
          $(".accordion div:first").css("display","block");


          //Change the show text to hide
          $(".accordion h6:first").find("span").html("&#x25BC;");
        }
        else {
          $(".accordion div").addClass("close");
        }


        // Bind the click function to the H3 element
        $(".accordion h6").click(function(e){

          // prevent the anchor tag from doing anything
          e.preventDefault();


          // Find the content of the accordion that has just been opened
          var $accordionContent = $(this).next("div");
          //Only call $.slideToggle() to open or close the content if it is not currently being animated:
          $accordionContent.not(":animated").slideToggle();

          // Toggle the aria-expanded
          // The value of attrAriaExpanded is a string, not a bool, so true has to be in quotes in the comparison
          if($accordionContent.attr("class") === "close") { // div was closed, it is being opened

            $accordionContent.removeClass("close");

            // update the button label
            $(this).find("span").html("&#x25BC;");

          }
          else { // div was opened, it is being closed
            $accordionContent.addClass("close");
            // update the button label
            $(this).find("span").html("&#x25B6;");

          }

        });

         return false;
      }

      $(document).ready(function(){

        cfpbAccordion(true);

      });

 // Tags's "more" link

function OpenDiv(id){
document.getElementById(id).style.height = "auto";
}

$("a.moretags").click(function ( event ) {
      event.preventDefault();
      $(this).hide();
    });

/* End Newsroom */
