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

function hideMenu() {
    $(".active").removeClass("active");
    $("#closeMenu").remove();
    $("#subnav nav").slideUp();
}

/* trigger when page is ready */
$(document).ready(function (){
    skipNav();
    $("#header nav a").mouseenter(function() {
        window.clearTimeout(hidemenu);
        var target = $(this).attr("href");
        if (($(target).css("display") == "none") || (target == "/")) {
            hideMenu();
            linkElement = this;
            dropdown = window.setTimeout(dropMenu, 500);
        }
        else {

        }
        return false;
    }).mouseleave(function() {
        hidemenu = window.setTimeout(hideMenu, 500);
        window.clearTimeout(dropdown);
        dropdown = 0;
    }).click(function(e) {
        if(dropping) {
            return false;
        }
        var clicked = $(this);
        var target = clicked.attr("href");
        if(target == "/") {
            return true;
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
    $(".signup,.signup2").submit(function() {
        var form = $(this);
        form.children("fieldset").children("p:last-child").children("button").attr("disabled","disabled");

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
                        thanks = "Thanks, we'll be in touch.";
                    }
                    form.html("<p>"+thanks+"</p>");
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
        $(this).attr("src",url+"?wmode=transparent")
    });
    $('a[href$="pdf"]').each(function() {
        $(this).addClass("pdf");
    });
});

/* Skip nav to primary content link */

function skipNav() {
    var $skipLink = $('#skip-link');
    $skipLink.click(function() {
        $('#primary-content').focus();
    });
}


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
