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
    
    $('.button-link').click(function(){
        _gaq.push(['_trackEvent', 'Suggest a Question', 'Add a New Question Link']);
    });
    
    $('#submit-question').submit(function(){
        _gaq.push(['_trackEvent', 'Suggest a Question', 'Final Suggestion Button']);
    });
    
    $('#tellyourstory').click(function(){
        _gaq.push(['_trackEvent', 'Tell Us Your Story', 'Tell Us Your Story Link']);
    });
    
    $('#complaintlink').click(function(){
        _gaq.push(['_trackEvent', 'File a Complaint', 'Submit a Complaint Link']);
    });
    
    $(".internal-link").click(function(){
    	var link_text = $(this).text();
        var link_url = $(this).attr('href')
        _gaq.push(['_trackEvent', 'Internal Link', link_text, link_url]);
    });
    
    $('.internal-page-link').click(function(){
        var link_url = $(this).attr('href')
        _gaq.push(['_trackEvent', 'Internal Link', 'In Page Navigation', link_url]);
    });
    
    $('.exit-link').click(function(){
        var link_url = $(this).attr('href')
        _gaq.push(['_trackEvent', 'Exit Link', 'Exit Link', link_url]);
    });
    
    $('.apply-link').click(function(){
        var link_url = $(this).attr('href')
        _gaq.push(['_trackEvent', 'Exit Link', 'Apply Link', link_url]);
    });
    
    $('.email-link').click(function(){
        var link_url = $(this).attr('href')
        _gaq.push(['_trackEvent', 'Contact', 'Email', link_url]);
    });
    
    $('.phone-link').click(function(){
        var link_url = $(this).attr('href')
        _gaq.push(['_trackEvent', 'Contact', 'Telephone', link_url]);
    });
  
});