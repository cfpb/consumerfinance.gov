'use strict';
var paginationContent = element( by.css( '.m-pagination' ) );

var pagination = {

  paginationContent: paginationContent,

  form: paginationContent.element( by.css( 'form' ) ),

  previousBtn:
    paginationContent.element( by.css( '.m-pagination_btn-prev' ) ),

  nextBtn:
    paginationContent.element( by.css( '.m-pagination_btn-next' ) ),

  pageInput:
    paginationContent.element( by.css( '.m-pagination_current-page' ) ),

  pageBtn:
    paginationContent.element( by.css( '.m-pagination_submit-btn' ) )

};

module.exports = pagination;
