
function show_error(frm, text){
    $('#email-error-box').append($('<div />').addClass('err').html(text).css('display', 'none').fadeIn());
    return false;
}


function smooth_scroll(id){
    $('html,body').animate({scrollTop:$('#' + id).offset().top}, 700);
    return false;
}

$(document).ready(function(){
    $('.goto-jobs').click(function(){
        smooth_scroll('featured_positions');
    });


    $('#email_collection_form #email').focus(function(){
        $('#email-error-box .err').delay(400).slideUp();
    });

    // tie enter keydown to form submission:
    $('#email').keydown(function(e){
        if(e.which == 13){
            $('#signup_for_update').click();
            return false;
        }
    });


    $('#signup_for_update').click(function(){
        var form = $('#email_collection_form');
        // clear errors
        form.find('.err').remove();

        if(!(/^([a-zA-Z0-9_\.\-\+])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/.test($('#email').val())))
            return show_error(form, 'Please provide a valid email address and try again!');

        $.ajax({
            type: "POST",
            url: "/subscriptions/new/",
            data: form.serialize(),
            complete: function(req, status_msg) {
                if(status_msg == 'success')
                    form.addClass('success').html('Thank you for providing us your email address. You will receive updates from us shortly.');
                else
                    return show_error(form, 'There was an issue with your submission. Please try again later!');
            }
        });
        return false;
    });

    setup_decision_tree();
});

function setup_decision_tree(){
    $('.decision-tree').each(function(i,n){
        $(n).find('.dec-answer span').click(function(){
            $(this).parent().find('.sel').removeClass('sel');
            $(this).addClass('sel');

            // notify its respective function
            var decision_tree_root = $(this).closest('.decision-tree');
            if(decision_tree_root)
                tree_decide(decision_tree_root);
        });
    });

    // activating the form
    $('.launch_decision_tree').click(function(){
        var $this = $(this);
        var target_tree_id = $this.attr('target_tree');
        $(this).addClass('header_look');
        $('#' + target_tree_id).slideDown();
    });

    // cancel button
    $('.cancel-button').click(function(){
        var $this = $(this);
        var dec_tree_nd = $this.closest('.decision-tree');

        $this.closest('.decision-tree').parent().find('.header_look').removeClass('header_look');
        $(dec_tree_nd).slideUp();
        return false;
    });

    // show the tooltip if the form is incomplete
    $('.next-step-btn').mouseover(function(){
        if($(this).hasClass('button-disabled')){
            $(this).find('.incomplete-tooltip').fadeIn(200);
        }
    });

    $('.next-step-btn').mouseout(function(){
        $(this).find('.incomplete-tooltip').fadeOut(100);
    });

    $('.next-step-btn').click(function(){
        if(!$(this).hasClass('button-disabled')){
            document.location = $(this).data('url');
        }
    });
}

var dec_urls = {
    'manager_dec_tree':{
        '00':'https://usajobs.gov/GetJob/ViewDetails/315271600',
        '01':'https://usajobs.gov/GetJob/ViewDetails/315271200',
        '10':'https://usajobs.gov/GetJob/ViewDetails/315271800',
        '11':'https://usajobs.gov/GetJob/ViewDetails/315271800'
    }
};


function tree_decide(nd){
    var id = nd[0].id;
    var selections = nd.find('.dec-answer .sel');

    if(selections.length != 2){
        nd.find('.next-step-btn').addClass('button-disabled');
        return false;
    }else{
        nd.find('.next-step-btn').removeClass('button-disabled');
    }

    var url = dec_urls[id][($(selections[0]).text() == 'Yes'?'1':'0') + ($(selections[1]).text() == 'Yes'?'1':'0')];
    nd.find('.next-step-btn').data('url', url);
}
