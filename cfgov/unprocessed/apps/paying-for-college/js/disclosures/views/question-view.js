// TODO: Remove jquery.
const $ = require( 'jquery' );

const Analytics = require( '../utils/Analytics' );
const postVerification = require( '../dispatchers/post-verify' );
const getFinancial = require( '../dispatchers/get-financial-values' );
const getSchool = require( '../dispatchers/get-school-values' );
const getDataLayerOptions = Analytics.getDataLayerOptions;

const questionView = {
  $settlementBigQuestion: $( '.step_settlement' ),
  $nonsettlementBigQuestion: $( '.step_nonsettlement' ),
  $getOptions: $( '.get-options' ),
  $followupNoNotSure: $( '.followup__no-not-sure' ),
  $followupYes: $( '.followup__yes' ),
  $optionsWrapper: $( '.get-options__dynamic' ),
  $options: $( '.option' ),
  $optionsSidebar: $( '.get-options_sidebar' ),
  $transferCredits: $( '.option__transfer-credits' ),
  $exploreSchools: $( '.option__explore-schools' ),
  $workWhileStudying: $( '.option__work-while-studying' ),
  $takeAction: $( '.option__take-action' ),
  $nextSteps: $( '.next-steps' ),
  $feedback: $( '.feedback' ),

  /**
   * Initiates the object
   */
  init: function() {
    const settlementStatus =
      getSchool.values().settlementSchool || false;

    this.displayOptions( settlementStatus );
    this.bigQuestionListener( settlementStatus );
  },

  /**
   * Show the appropriate content in Step 3 for settlement schools
   * @param {boolean} isSettlementStatus Flag if this is a settlement school
   */
  displayOptions: function( isSettlementStatus ) {
    if ( isSettlementStatus === true ) {
      questionView.$settlementBigQuestion.show();
      questionView.$nonsettlementBigQuestion.hide();
      $( '#question_answer-no' ).hide();
      questionView.$optionsWrapper.addClass(
        'get-options__settlement content_main' );
      questionView.$optionsWrapper.addClass(
        'get-options__settlement content_main' );
      questionView.$transferCredits.remove();
      questionView.$exploreSchools.remove();
      questionView.$takeAction.remove();
      questionView.$options.addClass( 'option__settlement' );
      questionView.$optionsSidebar.show();
      questionView.$optionsWrapper.removeClass( 'get-options__dynamic' );
    } else {
      questionView.$settlementBigQuestion.hide();
      questionView.$nonsettlementBigQuestion.show();
      questionView.$workWhileStudying.remove();
      questionView.$optionsSidebar.remove();
    }
  },

  /**
   * Listener function for the "big question"/"moment of pause" buttons
   * @param {boolean} isSettlementStatus Flag if this is a settlement school
   */
  bigQuestionListener: function( isSettlementStatus ) {
    const $answerButtons = $( '.question_answers > button' );
    $answerButtons.on( 'click', function() {
      const values = getFinancial.values();
      if ( isSettlementStatus === true ) {
        postVerification.verify( values.offerID, values.schoolID, false );
      }
      $answerButtons.removeClass( 'active' );
      $( this ).addClass( 'active' );

      if ( isSettlementStatus === true ) {
        questionView.$followupYes.hide();
        questionView.$followupNoNotSure.hide();
      } else if ( $( this ).attr( 'id' ) === 'question_answer-yes' ) {
        questionView.$followupYes.show();
        questionView.$followupNoNotSure.hide();
      } else {
        questionView.$followupNoNotSure.show();
        questionView.$followupYes.hide();
      }
      // Show the rest of the page
      questionView.$getOptions.show();
      questionView.$nextSteps.show();
      questionView.$feedback.show();
      $( 'html, body' ).stop().animate( {
        scrollTop: questionView.$getOptions.offset().top - 120
      }, 900, 'swing', function() {
        // Noop function.
      } );

      Analytics.sendEvent( getDataLayerOptions( 'Step Completed',
        $( this ).text().trim() )
      );
    } );
  }

};

module.exports = questionView;
