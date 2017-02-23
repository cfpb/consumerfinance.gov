// using jQuery
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




var rating_switcher = function(serverAction, cssClass){
    return function(rating_button){
        var csrftoken = getCookie('csrftoken');
        rating_button.attr('class', 'kbfeedback processing')
        $.post(ratingManager, {action:serverAction, term:rating_button.data('term'), csrfmiddlewaretoken:csrftoken},
        function(data){ 
           if ( data.followup != null ){
               $.colorbox({href:data.followup});
           
               
           }

         rating_button.attr('class', 'kbfeedback '+ cssClass);
        }, dataType='json');
    }    
}

$(function(){
   $.post(sessionHistory, function(){
        var csrftoken = getCookie('csrftoken');
        $.post(ratingManager, {action:'count', csrfmiddlewaretoken:csrftoken})
        $.post(ratingManager, {action:'render',  csrfmiddlewaretoken:csrftoken},function(data){

          $('#rating').html(data);

            unselect_rating=rating_switcher('remove', 'unselected tag');
            select_rating=rating_switcher('add', 'selected tag')
            $('#itemrating a').click(function(rating_button){
        rating_button.preventDefault();
                var rb= $(rating_button.currentTarget)
                     if (rb.hasClass('selected')){
                         unselect_rating(rb);
                     } else {
                         select_rating(rb);
                     }  
                 

              }); 

              $(document).on('submit','#followup', function(form){
          form.preventDefault();
                  formdata=$('#followup').serialize();
                  $.post(ratingManager, formdata, function(data){
                      $.colorbox.close();
                  }, dataType='json')
              })
       });
   });
});
