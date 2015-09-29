'use strict';

var pagination = {

  paginationContent: element.all( by.css( '#pagination_content' ) ),

  paginationResults:
  element.all( by.css( '#pagination_content .post-preview' ) ),

  paginationForm: element( by.css( '.pagination_form' ) ),

  paginationPrevBtn: element( by.css( '.pagination_prev' ) ),

  paginationNextBtn: element( by.css( '.pagination_next' ) ),

  paginationPageInput: element( by.css( '.pagination_current-page' ) )

};

module.exports = pagination;
