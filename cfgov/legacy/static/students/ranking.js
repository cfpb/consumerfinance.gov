$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

$(document).ready(function() {
  $(".ranking .inner").append('<img src="/static/students/drag_handle1.png" alt="move" class="handle">');
  $(".ranking input").hide();
  $("#rankinstructions").text("green handles");
  $("#comments").keyup(function(){
    limitChars('comments', '3000', 'charsleft');
  });
  $(".ranking").sortable({
    handle : '.handle',
    update : function() {
      var order=$(".ranking").sortable('serialize').split("&");
      for(var i = 0; i < order.length; i++) {
        $("#item_"+order[i].split("=")[1]).val(i+1);
      }
    }
  });
  $(".ranking").disableSelection();
  $("#rankForm").submit(function() {
    $("#getRanking").fadeOut();
    $("#commentbox").fadeOut();
    $("#spinbox").fadeIn();
    $(".handle").remove();
    var itemChildren = $(".ranking").children("li");
    itemChildren.appendTo($("#yourRanking"));
    $.post("/students/knowbeforeyouowe/rankserver/submit/",{
        id: "kbyo_sle",
        item_1: $("#item_1").val(),
        item_2: $("#item_2").val(),
        item_3: $("#item_3").val(),
        item_4: $("#item_4").val(),
        item_5: $("#item_5").val(),
        item_6: $("#item_6").val(),
        item_7: $("#item_7").val(),
        item_8: $("#item_8").val(),
        item_9: $("#item_9").val(),
        comments: $("#comments").val()
      }, function(json) {
           var results = json.results;
           var newItem;
           var newText;
           for( var j = 0; j < results.length; j++) {
             newItem = document.createElement("li");
             newText = document.createTextNode(results[j].description);
             newItem.appendChild(newText);
             $("#overallRanking").append(newItem);
           }
           $("#spinbox").fadeOut();
           $("#showResults").fadeIn();
         }, "json");
    return false;
  });
}); 
