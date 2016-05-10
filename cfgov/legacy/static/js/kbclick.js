$(function(){
    
    
    $('a.kbq').click(function(){
        
        $('body').append("<form method='post' id='clickquestion'><input name='return' type='hidden' value='" + document.location.href +"'> <input type='submit'/></form>" );
               
        
        form=$('#clickquestion');
        form.attr('action', $(this).attr('href'));
        form.submit();
        return false;
    })
    
})