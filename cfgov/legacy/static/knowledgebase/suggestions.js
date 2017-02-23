$(function(){

    $('#id_question').after("<div id='qfill'><ul/></div>");

    var last_value="";

    // There are jQuery and underscore debounce implementations but to avoid
    // dependency hell, I'm pasting in the underscore/lodash variant.
    // https://github.com/bestiejs/lodash/blob/v0.8.2/lodash.js#L3242

    function debounce(func, wait, immediate) {
      var args,
          result,
          thisArg,
          timeoutId;

      function delayed() {
        timeoutId = null;
        if (!immediate) {
          result = func.apply(thisArg, args);
        }
      }

      return function() {
        var isImmediate = immediate && !timeoutId;
        args = arguments;
        thisArg = this;

        clearTimeout(timeoutId);
        timeoutId = setTimeout(delayed, wait);

        if (isImmediate) {
          result = func.apply(thisArg, args);
        }
        return result;
      };
    }

    // Define a debounced function with a coalescing period of 500 ms.

    var sendQuestion = debounce(function(event) {
        var field = $('#id_question');
        if (field.val().length > 2){
            if (field.val() != last_value){
                var txt=field.val()
                last_value=txt;
                $.get('/askcfpb/api/search/',{q:txt}, function(data){
                   if (data['results'].length > 0){
                       var results= data['results'] ;
                       var qlist=$('#qfill ul');
                       qlist.empty();
                       for (index in results.slice(0,3)) {
                           var q=results[index]
                           qlist.append("<li><a href='"+ q.htmluri+"'>"+q.title+"</a></li>") 
                       }
                       
                   }
                    
                })
                
           } 
        }
        
    }, 500);

    // Bind the debounced function to the `keyup` event.

    $('#id_question').keyup( sendQuestion );
    
})
