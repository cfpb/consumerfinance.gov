(function ($) {

    $.fn.cf_pagination = function(userSettings){

        // Todo: Modify the URL using https://github.com/browserstate/history.js

        function submit(e, callback) {
            var action = getAjaxAction(e);

            e.preventDefault();

            $.when(getPaginatedPosts(action))
            .then(function(results) {
                updatePosts(results);
                callback(e);
            });
        }

        function updatePosts(results) {
            // Animation
            // $('#pagination_content')
            // .fadeOut(400, function(){
            //     $(this).replaceWith(results);
            //     $('#pagination_content')
            //     .hide()
            //     .fadeIn(400);
            // });
            // $('html,body').animate({scrollTop: $('#pagination_content').offset().top}, 800);

            // No animation
            $('#pagination_content').replaceWith(results);
            $('html,body').animate({scrollTop: $('.content_main').offset().top}, 0);
        }

        function getAjaxAction(e) {
            var action = '' + 
                         // Remove everything after the '?'
                         e.currentTarget.action.split('?')[0]
                         .replace('#pagination_content','') + // Remove '#pagination_content' so we can add it in the right spot
                         $(e.currentTarget).parents('.pagination').data('ajax-action') +
                         '?' +
                         $(e.currentTarget).serialize() +
                         '#pagination_content';
            return action;
        }

        function getPaginatedPosts(page) {
            var promise = $.get(page);
            return promise;
        }

        return $(this).each(function(){
            var settings = $.extend({
                        'callback': function(e){}
                    }, userSettings );

            $(this).on('submit', '.pagination_form', function(e){
                submit(e, settings.callback);
            })​;
        });
    };

}(jQuery));
