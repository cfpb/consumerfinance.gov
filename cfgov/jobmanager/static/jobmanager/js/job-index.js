// make job category filtering work
$(document).ready(function(){
    // map filter link's onclick to filtering function
    $('#job-search-methods a').click(function(){
        sel_job_filter(this.id);
    });
    
    // look at the current hash value and show
    // the right section.
    var hash_value = document.location.hash;
    if(hash_value)
        sel_job_filter(hash_value.replace('#', ''), 1);
});

// Toggles between job category types
// offers an optional smooth transition
// called directly by the filtering links
function sel_job_filter(link_id, anim_duration){
    link_id = link_id.replace('-link','');
    
    var cur_sect = $('#job-list-arena .sel');
    var cur_link = $('#job-search-methods .sel');
    var new_sect = $('#' + link_id + '-sect');
    var new_link = $('#' + link_id + '-link');
    
    // assert all elements exist and 
    // the link is not already selected
    if(!(cur_sect && cur_link && new_sect && new_link && cur_sect[0] != new_sect[0]))
        return;
    
    // set proper class-names for all elements
    cur_link.removeClass('sel');
    cur_sect.removeClass('sel');
    new_link.addClass('sel');
    new_sect.addClass('sel');
    
    // toggle between sections
    cur_sect.slideUp(anim_duration?anim_duration:'slow');
    new_sect.slideDown(anim_duration?anim_duration:'slow');
}