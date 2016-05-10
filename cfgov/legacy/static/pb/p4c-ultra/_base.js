
setTimeout(function(){
    $('#wizroot a, #wiz_templates a').each(function(i, n){
        var $n=$(n);
        $n.attr('target', '_blank');
    });
}, 500);