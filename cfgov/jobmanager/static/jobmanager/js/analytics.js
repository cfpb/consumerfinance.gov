
$(function(){
    $('.share-facebook').click(function(){
        _gaq.push(['_trackEvent', 'Share', 'Facebook']);
    });
    $('.share-twitter').click(function(){
        _gaq.push(['_trackEvent', 'Share', 'Twitter']);
    });
    $('.share-email').click(function(){
        _gaq.push(['_trackEvent', 'Share', 'Email']);
    });
    
    
    $('#submit-question').submit(function(){
        _gaq.push(['_trackEvent', 'Suggest a Question', 'Final Suggestion Button']);
    });
    
    
    
    
  
});