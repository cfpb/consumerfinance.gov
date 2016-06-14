var public_loan = 0;
var private_loan = 0;
var can_pay = 0;
var cont_ed = 0;

/*function setHeight(which) {
  var div = $(which);
  div.css({height: div.height()});
}*/


$(document).ready(function() {
  $("#public").click(function(e) {
    e.preventDefault();
    public_loan = 1;
    private_loan = 0;
    $("#ques1").slideUp();
    /*setHeight("#ques2");*/
    $("#ques2").slideDown();
    $('html, body').animate({scrollTop:350}, 'slow');
  });
  $("#private").click(function(e) {
    e.preventDefault();
    public_loan = 0;
    private_loan = 1;
    $("#ques1").slideUp();
    /*setHeight("#ques2");*/
    $("#ques2").slideDown();
    $('html, body').animate({scrollTop:350}, 'slow');
  });
  $("#both").click(function(e) {
    e.preventDefault();
    public_loan = 1;
    private_loan = 1;
    $("#ques1").slideUp();
    /*setHeight("#ques2");*/
    $("#ques2").slideDown();
    $('html, body').animate({scrollTop:350}, 'slow');
  });
  $("#yes").click(function(e) {
    e.preventDefault();
    can_pay = 1;
    $("#ques2").slideUp();
    /*setHeight("#direct_debit");*/
    $("#direct_debit").slideDown();
    $('html, body').animate({scrollTop:350}, 'slow');
  });
  $(".no").click(function(e) {
    e.preventDefault();
    if(public_loan) {
      $("#ques2").slideUp();
      /*setHeight("#ques3");*/
      $("#ques3").slideDown();
      $('html, body').animate({scrollTop:350}, 'slow');
    }
    else {
      $("#ques2").slideUp();
      /*setHeight("#call_servicer");*/
      $("#call_servicer").slideDown();
      $('html, body').animate({scrollTop:350}, 'slow');
    }
  });
  $("#yes2").click(function(e) {
    e.preventDefault();
    $("#ques3").slideUp();
    /*setHeight("#defer");*/
    $("#defer").slideDown();
    /*setHeight("#ibr");*/
    $("#ibr").slideDown();
    if(private_loan) $("#call_servicer").slideDown();
    $('html, body').animate({scrollTop:350}, 'slow');
  });
  $("#no2").click(function(e) {
    e.preventDefault();
    $("#ques3").slideUp();
    /*setHeight("#ibr");*/
    $("#ibr").slideDown();
    if(private_loan) $("#call_servicer").slideDown();
    $('html, body').animate({scrollTop:350}, 'slow');
  });
  $(".backtrack").click(function(e) {
    e.preventDefault();
    $(".question").slideUp();
    /*setHeight($(this).attr("href"));*/
    $($(this).attr("href")).slideDown();
    $('html, body').animate({scrollTop:350}, 'slow');
  });
});