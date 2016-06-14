$(function() {
    $('.hero a[href^="http://youtu.be"]').cfpbVideoReplace();
    $('.js-showtoggle').cfpbShowToggle();
    $('.ui-autocomplete-input').cfpbInputFilledCheck();
    $('.ac-search-form').appendAround();
    $('.share.s-show-on-small > span').appendAround();
    $('#js-ac-qrating-not-helpful').cfpbSimpleFormPost();
    $('#js-ac-qrating-helpful').cfpbSimpleFormPost({ 'resultsTarget': '.js-simpleform-results-share' });
});
