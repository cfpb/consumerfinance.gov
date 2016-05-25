
$(function() {
    /* this allows us to pass in HTML tags to autocomplete. Without this they get escaped 
    http://www.arctickiwi.com/blog/jquery-autocomplete-labels-escape-html-tags
    */
    $[ "ui" ][ "autocomplete" ].prototype["_renderItem"] = function( ul, item) {
    return $( "<li></li>" ) 
      .data( "item.autocomplete", item )
      .append( $( "<a></a>" ).html( item.label ) )
      .appendTo( ul );
    };
    
    
        $( "#ac-search #q, #ac-search #id_q" ).autocomplete({
            source: function(request, response){
                var data_uri=searchAPI
                
                
                $.getJSON(data_uri, request, function(data){
                    var term = request.term;
                    response(data);
                })
                
            },
            select: function(event, ui) { 
                document.location=ui.item.uri;
                return false;
                },
            minLength:3
            });
    });

