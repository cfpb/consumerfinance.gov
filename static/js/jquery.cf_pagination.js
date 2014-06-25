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
            $('#pagination_content')
            .fadeOut(400, function(){
                $(this).replaceWith(results);
                $('#pagination_content')
                .hide()
                .fadeIn(400);
            });

            // No animation
            // $('#pagination_content').replaceWith(results);
        }

        function getAjaxAction(e) {
            var action = $(e.currentTarget).parents('.pagination').data('ajax-action') +
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
            });
        });
    };

}(jQuery));
