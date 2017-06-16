'use strict';
var paginationContent = element( by.css( '.m-pagination' ) );

var pagination = {

  paginationContent:
    paginationContent,

  paginationForm:
    paginationContent.element( by.css( 'form' ) ),

  paginationPrevBtn:
    paginationContent.element( by.css( '.m-pagination_btn-prev' ) ),

  paginationNextBtn:
    paginationContent.element( by.css( '.m-pagination_btn-next' ) ),

  paginationPageInput:
    paginationContent.element( by.css( '.m-pagination_current-page' ) ),

  paginationPageBtn:
    paginationContent.element( by.css( '.m-pagination_btn-submit' ) )

};

module.exports = pagination;
